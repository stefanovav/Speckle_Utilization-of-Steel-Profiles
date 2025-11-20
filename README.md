***THIS PROJECT IS WRITTEN WITH AN OLD SPECKLE SDK***
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


2. send_data_to_speckle(height, width, length, stream_id, speckle_token, res)
Description: Updates the dimensions of the geometry data and sends it to the Speckle server.


3. fetch_data_from_speckle(stream_id, commit_id, speckle_token)
Description: Fetches data from the Speckle server for a specific stream and commit.


4. parse_dimensions_from_commit(client, stream_id, commit_id, speckle_token)
Description: Parses dimensions (height, width, length) from the commit object.


5. parse_data_from_commit(client, stream_id, commit_id, speckle_token)
Description: Parses material data from the commit object.


6. add_materials_data(sublist, material_key)
Description: Adds material data to items in the sublist based on a specified key.


7. commit2viewer(stream_id, commit_id, speckle_token)
Description: Embeds the Speckle viewer in the Streamlit app to display a specific commit.


8. transform_keys_to_integers(obj)
Description: Recursively transforms dictionary keys from @{0} to integers for display.


9. extract_combined_data(members_list)
Description: Extracts Key, Utilization, and CrossSection data from the Members list.


10. display_combined_table(combined_data)
Description: Displays the combined Key, Utilization, and CrossSection data in a Plotly table.



**Running the Application**

main(): Orchestrates the workflow of fetching data, updating it, sending it back to Speckle, and displaying results.

Functionality:

Retrieves the latest commit ID from a file.

Authenticates with Speckle using a provided token.

Allows user input for dimensions and key to set the material.

Sends updated data to Speckle.

Fetches data from Speckle and displays it.

Embeds the Speckle viewer to display the commit.


## License

This project is licensed under the MIT License - see the [LICENSE] file for details.

