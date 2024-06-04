# Speckle Utilization of Steel Profiles

This repository contains the code for a Streamlit application that interacts with Speckle to fetch and send data related to the utilization of steel profiles. The application allows users to input dimensions, retrieve data about the model from Speckle, and visualize and update the data. 
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

1. get_latest_commit_id(file_path)
Description: Retrieves the latest commit ID from a specified file.

Parameters:
file_path (str): The path to the file containing the commit ID.
Returns: The commit ID as a string, or None if the file is not found.

2. send_data_to_speckle(height, width, length, stream_id, speckle_token, res)
Description: Updates the dimensions of the geometry data and sends it to the Speckle server.

Parameters:
height (float): The height to be set for the geometry.
width (float): The width to be set for the geometry.
length (float): The length to be set for the geometry.
stream_id (str): The ID of the Speckle stream.
speckle_token (str): The Speckle token for authentication.
res (Base): The received data from Speckle.
Returns: The new commit ID as a string, or None if an error occurs.

3. fetch_data_from_speckle(stream_id, commit_id, speckle_token)
Description: Fetches data from the Speckle server for a specific stream and commit.

Parameters:
stream_id (str): The ID of the Speckle stream.
commit_id (str): The ID of the Speckle commit.
speckle_token (str): The Speckle token for authentication.
Returns: A tuple containing the stream and commit objects, or (None, None) if an error occurs.

4. parse_dimensions_from_commit(client, stream_id, commit_id, speckle_token)
Description: Parses dimensions (height, width, length) from the commit object.

Parameters:
client (SpeckleClient): The Speckle client.
stream_id (str): The ID of the Speckle stream.
commit_id (str): The ID of the Speckle commit.
speckle_token (str): The Speckle token for authentication.
Returns: A tuple containing the height, width, and length as floats, or (0, 0, 0) if an error occurs.

5. parse_data_from_commit(client, stream_id, commit_id, speckle_token)
Description: Parses material data from the commit object.

Parameters:
client (SpeckleClient): The Speckle client.
stream_id (str): The ID of the Speckle stream.
commit_id (str): The ID of the Speckle commit.
speckle_token (str): The Speckle token for authentication.
Returns: A list of dictionaries containing parsed material data, or an empty list if an error occurs.

6. add_materials_data(sublist, material_key)
Description: Adds material data to items in the sublist based on a specified key.

Parameters:
sublist (list): The list of items to which material data will be added.
material_key (str): The key used to determine which material to add.
Returns: The modified sublist with added material data.

7. commit2viewer(stream_id, commit_id, speckle_token)
Description: Embeds the Speckle viewer in the Streamlit app to display a specific commit.

Parameters:
stream_id (str): The ID of the Speckle stream.
commit_id (str): The ID of the Speckle commit.
speckle_token (str): The Speckle token for authentication.
Returns: None.

8. transform_keys_to_integers(obj)
Description: Recursively transforms dictionary keys from @{0} to integers for display.

Parameters:
obj (dict or list): The object whose keys will be transformed.
Returns: The transformed object.

9. extract_combined_data(members_list)
Description: Extracts Key, Utilization, and CrossSection data from the Members list.

Parameters:
members_list (list): The list of members from which data will be extracted.
Returns: A list of dictionaries containing combined data.

10. display_combined_table(combined_data)
Description: Displays the combined Key, Utilization, and CrossSection data in a Plotly table.

Parameters:
combined_data (list): The list of combined data to be displayed.
Returns: None.


**Running the Application**

main(): Orchestrates the workflow of fetching data, updating it, sending it back to Speckle, and displaying results.


## License

This project is licensed under the MIT License - see the [LICENSE] file for details.

