import Materials
import plotly.graph_objects as go
import streamlit as st
from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.transports.server import ServerTransport
from specklepy.api.credentials import get_account_from_token
from Materials import SteelS355, SteelS235
from specklepy.objects import Base
import os
import copy
import streamlit.components.v1 as components

# Instantiate material mappings
MATERIALS_MAPPING1 = SteelS355()
MATERIALS_MAPPING2 = SteelS235()

# Speckle server configuration
HOST = "speckle.xyz"
STREAM_ID = "f8ed39586f"
COMMIT_FILE_PATH = r"C:\[...]CommitPath.txt"  # Update with your file path

def get_latest_commit_id(file_path):
    """Retrieve the latest commit ID from a file."""
    try:
        with open(file_path, 'r') as f:
            commit_id = f.read().strip()
        return commit_id
    except FileNotFoundError:
        st.error("Commit ID file not found.")
        return None

def send_data_to_speckle(height, width, length, stream_id, speckle_token, res):
    client = SpeckleClient(host=HOST)
    account = get_account_from_token(speckle_token, HOST)
    client.authenticate_with_account(account)

    # Retrieve the Geometry data
    geometry_data = getattr(res, "Geometry", None)
    if not geometry_data:
        st.error("Geometry data not found in the received data.")
        return None

    sublist = getattr(geometry_data, "@{0}", None)
    if sublist:
        # Update the values of Width, Length, and Height
        sublist[0]['Width'] = width
        sublist[0]['Length'] = length
        sublist[0]['Height'] = height

        # Update the modified sublist in the Geometry data
        setattr(geometry_data, "@{0}", sublist)


        # Create a new Base object with the modified data
        base = Base(Geometry=geometry_data)
        transport = ServerTransport(client=client, stream_id=stream_id)
        obj_id = operations.send(base, [transport])

        # Create a new commit with the updated data
        new_commit_id = client.commit.create(
            stream_id=stream_id,
            object_id=obj_id,
            branch_name="main",
            message=f"Updated dimensions: height={height}, width={width}, length={length}"
        )

        return new_commit_id
    else:
        st.error("Sublist not found in the received data.")
        return None

@st.cache_data
def fetch_data_from_speckle(stream_id, commit_id, speckle_token):
    """Fetch data from the Speckle server."""
    client = SpeckleClient(host=HOST)

    if not speckle_token:
        st.error("Speckle token is not set. Please enter the SPECKLE_TOKEN.")
        return None, None

    try:
        account = get_account_from_token(speckle_token, HOST)
        client.authenticate_with_account(account)
        st.success("Successfully authenticated with Speckle.")
    except Exception as e:
        st.error(f"Failed to authenticate with Speckle: {e}")
        return None, None

    try:
        stream = client.stream.get(stream_id)
        commit = client.commit.get(stream_id, commit_id)
        return stream, commit
    except Exception as e:
        st.error(f"Failed to fetch stream or commit: {e}")
        return None, None


def parse_dimensions_from_commit(client, stream_id, commit_id, speckle_token):
    """Parse dimensions from the commit object."""
    try:
        # Authenticate client if necessary
        account = get_account_from_token(speckle_token, HOST)
        client.authenticate_with_account(account)

        # Fetch the commit object using the commit ID
        commit = client.commit.get(stream_id, commit_id)
        referenced_object_id = commit.referencedObject
        transport = ServerTransport(client=client, stream_id=stream_id)
        res = operations.receive(referenced_object_id, transport)

        # Assuming dimensions are stored in the commit data under Geometry -> @0
        geometry_data = getattr(res, "Geometry", None)
        if geometry_data:
            sublist = getattr(geometry_data, "@{0}", None)
            if sublist:
                fetched_height = sublist[0].Height if hasattr(sublist[0], 'Height') else 0
                fetched_width = sublist[0].Width if hasattr(sublist[0], 'Width') else 0
                fetched_length = sublist[0].Length if hasattr(sublist[0], 'Length') else 0
                return fetched_height, fetched_width, fetched_length

        return 0, 0, 0  # Default if dimensions not found
    except Exception as e:
        st.error(f"Error parsing dimensions from commit: {e}")
        return 0, 0, 0

def parse_data_from_commit(client, stream_id, commit_id, speckle_token):
    """Parse material data from the commit object."""
    try:
        # Authenticate client if necessary
        account = get_account_from_token(speckle_token, HOST)
        client.authenticate_with_account(account)

        # Fetch the commit object using the commit ID
        commit = client.commit.get(stream_id, commit_id)
        referenced_object_id = commit.referencedObject
        transport = ServerTransport(client=client, stream_id=stream_id)
        res = operations.receive(referenced_object_id, transport)

        # Getting data for the members of the commit in the list Members -> @0
        members_data = getattr(res, "Members", None)
        if members_data:
            sublist = getattr(members_data, "@{0}", None)
            if sublist:
                parsed_data = []
                for item in sublist:
                    key = getattr(item, 'Key', 'N/A')
                    utilization = getattr(item, 'Utilization', 'N/A')
                    cross_section = getattr(item, 'CrossSection', 'N/A')
                    material = getattr(item, 'Material', "S235",)
                    parsed_data.append({
                        'Key': key,
                        'Utilization': utilization,
                        'CrossSection': cross_section,
                        'Material': material
                    })
                return parsed_data

        return []  # Default if material data not found
    except Exception as e:
        st.error(f"Error parsing material data from commit: {e}")
        return []

def add_materials_data(sublist: list, material_key: str) -> list:
    """Add material data to items in the sublist."""
    for item in sublist:
        item.Material = MATERIALS_MAPPING1 if item.Key.startswith(material_key) else MATERIALS_MAPPING2
    return sublist

def commit2viewer(stream_id, commit_id, speckle_token):
    """Embed Speckle viewer."""
    height = 600  # Default height for the viewer
    if commit_id:
        embed_src = f"https://speckle.xyz/embed?stream={stream_id}&commit={commit_id}&access_token={speckle_token}"
        st.write(f"Embed URL: {embed_src}")  # Debugging line to confirm embed URL
        components.iframe(embed_src, height=height, scrolling=True)
    else:
        st.error("Unable to display viewer: commit ID is not available.")

def transform_keys_to_integers(obj):
    """Recursively transform dictionary keys from '@{0}' to integers for display."""
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            try:
                new_key = int(k.strip('@{}'))
            except ValueError:
                new_key = k
            new_obj[new_key] = transform_keys_to_integers(v)
        return new_obj
    elif isinstance(obj, list):
        return [transform_keys_to_integers(item) for item in obj]
    else:
        return obj

def extract_combined_data(members_list):
    """Extract Key, Utilization, and CrossSection data from the Members list."""
    combined_data = []
    for item in members_list:
        key = getattr(item, 'Key', 'N/A')
        cross_section = getattr(item, 'CrossSection', None)
        material = getattr(item, 'Material', 'S235')
        #material_strength = getattr(material, 'strength', 'N/A')  # Access strength property
        utilization = getattr(item, 'Utilization', None)
        combined_data.append({
            'Key': key,
            'CrossSection': cross_section,
            'Utilization': utilization,
            'Material': material
        })
    return combined_data

def display_combined_table(combined_data):
    """Display the combined Key, Utilization, and CrossSection data in a Plotly table."""
    if not combined_data:
        st.error("No data available.")
        return

    # Calculate the height dynamically based on the number of rows
    num_rows = len(combined_data)
    row_height = 30  # Adjust this value as needed
    table_height = num_rows * row_height

    header_values = list(combined_data[0].keys())
    cell_values = [list(col) for col in zip(*[list(row.values()) for row in combined_data])]

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=header_values,
            fill_color='paleturquoise',
            align='left',
            font=dict(size=16)  # Set header font size to 16
        ),
        cells=dict(
            values=cell_values,
            fill_color='#F5F5F5',
            align='left',
            font=dict(size=14)  # Set cell font size to 14
        )
    )])

    # Update the layout to adjust the height
    fig.update_layout(
        height=table_height,
        margin=dict(t=0, b=0, pad=0)
    )

    st.plotly_chart(fig)


def main():
    global COMMIT_FILE_PATH

    st.title("Speckle Utilization of Steel Profiles")

    # Add custom CSS for background color
    st.markdown(
        """
        <style>
        .stApp {
            background-color: lavender;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Get the latest commit ID from the file
    COMMIT_ID = get_latest_commit_id(COMMIT_FILE_PATH)
    if not COMMIT_ID:
        st.error("Failed to retrieve the latest commit ID.")
        return

    # Enter Speckle Token
    speckle_token = os.environ.get("SPECKLE_TOKEN")
    SPECKLE_TOKEN = st.text_input("Enter Speckle Token:", value=speckle_token)
    st.write("Entered Speckle Token:", SPECKLE_TOKEN)

    # User inputs for height, width, and length
    height = st.number_input("Enter Height, [m]:", min_value=1.0, step=0.1)
    width = st.number_input("Enter Width, [m]:", min_value=1.0, step=0.1)
    length = st.number_input("Enter Length, [m]:", min_value=1.0, step=0.1)

    # User input for material mapping key
    material_key = st.text_input("Enter First Character of ElementID (Key) (this group of elements is getting Steel S355, else S235):")

    if st.button("Send Data to Speckle"):
        if SPECKLE_TOKEN:
            stream, commit = fetch_data_from_speckle(STREAM_ID, COMMIT_ID, SPECKLE_TOKEN)
            if not stream or not commit:
                st.error("Failed to fetch stream or commit. Please check your Speckle server setup.")
                return

            client = SpeckleClient(host=HOST)
            account = get_account_from_token(SPECKLE_TOKEN, HOST)
            client.authenticate_with_account(account)

            transport = ServerTransport(client=client, stream_id=STREAM_ID)


    # Fetch data from Speckle server
    stream, commit = fetch_data_from_speckle(STREAM_ID, COMMIT_ID, SPECKLE_TOKEN)
    if not stream or not commit:
        st.error("Failed to fetch stream or commit. Please check your Speckle server setup.")
        return

    st.write("Stream Name:", stream.name)
    st.write("Commit Message:", commit.message)

    try:
        client = SpeckleClient(host=HOST)
        account = get_account_from_token(SPECKLE_TOKEN, HOST)
        client.authenticate_with_account(account)
        st.write("Successfully authenticated with Speckle for sending data.")

        transport = ServerTransport(client=client, stream_id=STREAM_ID)
        res = operations.receive(commit.referencedObject, transport)

        if res:
            # Transform data for display
            transformed_res = transform_keys_to_integers(copy.deepcopy(res))
            st.write("Transformed Data for Display:", transformed_res)

            # Modify original data structure with materials for Members list
            members_list = getattr(res, "Members", None)
            if members_list:
                sublist = getattr(members_list, "@{0}", None)
                if sublist:
                    sublist = add_materials_data(sublist, material_key)
                    setattr(members_list, "@{0}", sublist)


            # Modify original data structure with dimensions for the whole model
            geometry_list = getattr(res, "Geometry", None)
            if geometry_list:
                sublist = getattr(geometry_list, "@{0}", None)
                if sublist:
                    sublist[0]['Width'] = width
                    sublist[0]['Length'] = length
                    sublist[0]['Height'] = height
                    setattr(geometry_list, "@{0}", sublist)

                    # Create a new Base object with the modified data for Members and Geometry lists
                    base = Base(Members=members_list, Geometry=geometry_list)
                    obj_id = operations.send(base, [transport])
                    st.write("Data successfully sent to Speckle. Object ID:", obj_id)
                else:
                    st.error("Sublist not found in the received geometry data.")
            else:
                st.error("Geometry list not found in the received data.")

            # Verify the latest commit from the stream
            latest_commits = client.commit.list(STREAM_ID)
            latest_commit = latest_commits[0] if latest_commits else None

            if latest_commit:
                latest_commit_id = latest_commit.id
                st.write("Latest (updated) Commit ID:", latest_commit_id)
                commit2viewer(STREAM_ID, latest_commit_id, SPECKLE_TOKEN)
            else:
                st.error("No commits found in the stream.")

            st.write("Latest Commit ID:", latest_commit_id)


            # Display the updated dimensions after the data has been received and updated in Speckle

            fetched_height, fetched_width, fetched_length = parse_dimensions_from_commit(client, STREAM_ID, COMMIT_ID, SPECKLE_TOKEN)
            st.write("Updated Dimensions:")
            st.write("Height:", fetched_height)
            st.write("Width:", fetched_width)
            st.write("Length:", fetched_length)

            # Create a new commit with the updated data
            try:
                new_commit_id = client.commit.create(
                    stream_id=STREAM_ID,
                    object_id=obj_id,
                    branch_name="main",
                    message=f"updated commit within Grasshopper, based on commit {COMMIT_ID}"
                )

                # Fetch data from commit
                parsed_data = parse_data_from_commit(client, STREAM_ID, COMMIT_ID, speckle_token)

                # Display combined data
                display_combined_table(parsed_data)


            except Exception as e:
                st.error(f"Error creating new commit: {e}")

    except Exception as e:
        st.error(f"Error processing data: {e}")

if __name__ == "__main__":
    main()






