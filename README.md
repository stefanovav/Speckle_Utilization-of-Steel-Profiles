# Speckle Utilization of Steel Profiles

This repository contains the code for a Streamlit application that interacts with Speckle to fetch and send data related to the utilization of steel profiles. The application allows users to input dimensions, retrieve data from Speckle, and visualize and update the data. 
The steel structure is built using Grasshopper with the Karamba3D plugin. The key role of the code is to ensure that all parties - Grasshopper, Streamlit and Speckle - are always working with the latest commit. 

**Features**

- Fetches data from a Speckle stream.
- Updates dimensions and material properties.
- Sends updated data back to Speckle.
- Displays data in a tabular format.
- Embeds a Speckle viewer for visual inspection.


**Configuration**

Set your Speckle token as an environment variable:


export SPECKLE_TOKEN=your-speckle-token
Update the COMMIT_FILE_PATH in app.py to the path of the file containing the commit ID:


COMMIT_FILE_PATH = r"C:\[...]"
Set your Speckle stream ID and host:


HOST = "speckle.xyz"
STREAM_ID = "32ea4a3d73"


streamlit run app.py

Open your web browser and navigate to the URL provided by Streamlit (usually http://localhost:8501).

Enter your Speckle token in the input field.

Enter the dimensions for height, width, and length.

Click the "Send Data to Speckle" button to update and send data.

View the fetched data, transformed data, and the embedded Speckle viewer.


**Main Components**

Speckle Server Configuration: Host, stream ID, and commit file path.

Authentication: Uses Speckle token for authentication.

Data Fetching: Retrieves data from Speckle.

Data Updating: Updates dimensions and material properties in the retrieved data.

Data Sending: Sends updated data back to Speckle.

Data Visualization: Displays data in a table and embeds the Speckle viewer.


**Functions**

get_latest_commit_id(file_path): Retrieves the latest commit ID from a file.

send_data_to_speckle(height, width, length, stream_id, speckle_token, res): Updates and sends data to Speckle.

fetch_data_from_speckle(stream_id, commit_id, speckle_token): Fetches data from Speckle server.

parse_dimensions_from_commit(client, stream_id, commit_id, speckle_token): Parses dimensions from the commit object.

add_materials_data(sublist): Adds material data to items in the sublist.

commit2viewer(stream_id, commit_id, speckle_token): Embeds Speckle viewer.

transform_keys_to_integers(obj): Transforms dictionary keys from '@{0}' to integers.

extract_combined_data(members_list): Extracts key, utilization, and cross-section data.

display_combined_table(combined_data): Displays data in a Plotly table.


**Running the Application**

main(): Orchestrates the workflow of fetching data, updating it, sending it back to Speckle, and displaying results.
