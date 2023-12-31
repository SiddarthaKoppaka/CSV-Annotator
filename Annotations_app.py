import streamlit as st
import pandas as pd
import base64

# Function to load data from a CSV file


def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Function to save data to a CSV file


def save_data(df, file_path):
    df.to_csv(file_path, index=False)

# Function to create a download link for a file


@st.cache_data
def create_download_link(df, file_name):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">Download CSV File</a>'
    return href

# Main function


def main():
    st.title("CSV Annotation Tool")

    # File selection
    file_path = st.file_uploader("Choose a CSV file", type="csv")
    file_name = file_path.name

    if file_path is not None:
        df = load_data(file_path)

        st.write("Total sentences:", len(df))

        # Initialize index and annotations
        index = st.session_state.get('index', 0)
        annotations = st.session_state.get('annotations', [None] * len(df))

        if index < len(df):
            # Get the current question and display it
            sentence = df.loc[index, 'Content']
            st.subheader("Sentence:")
            st.text(f'Sentence No - {index+1} :')
            st.write(sentence)

            # Annotation options
            annotation = st.radio('Annotaions : ', ('Positive', 'Negative', 'Irrelevant'))
            #print(annotation)

            # Save the annotation
            annotations[index] = annotation

            # Update the index
            index += 1

            # Store the index and annotations in session state
            st.session_state['index'] = index
            st.session_state['annotations'] = annotations

            # Show the navigation buttons
            col1, col2 = st.columns(2)

            with col1:
                # Show the next button
                next_button = st.button("Next Question")
                if next_button:
                    # Check if all questions are answered
                    if index >= len(df):
                        # Create a new DataFrame to store the annotations
                        annotated_df = pd.DataFrame(
                            {'Content': df['Content'], 'Annotation': annotations})

                        # Save the DataFrame to a new CSV file
                        save_path = st.text_input(
                            "Enter the path to save the annotated CSV file", "annotated_data.csv")
                        save_data(annotated_df, save_path)

                        # Provide a download link for the annotated CSV file
                        st.markdown(create_download_link(
                            annotated_df, f"{file_name}annotated.csv"), unsafe_allow_html=True)

                        # Show completion message
                        st.success("Annotation process completed.")

            with col2:
                # Show the Save and Download button
                if st.button("Save and Download"):
                    # Create a new DataFrame to store the annotations
                    annotated_df = pd.DataFrame(
                        {'Content': df['Content'], 'Annotation': annotations})

                    # Save the DataFrame to a new CSV file
                    save_path = st.text_input(
                        "Enter the path to save the annotated CSV file", "annotated_data.csv")
                    save_data(annotated_df, save_path)

                    # Provide a download link for the annotated CSV file
                    st.markdown(create_download_link(
                        annotated_df, f"{file_name}annotated.csv"), unsafe_allow_html=True)

                    # Show completion message
                    st.success("Annotations saved and downloaded.")

        # Check if annotations are available
        #if any(annotations):
            # Provide a download link for the current annotations
            #if st.button("Download Current Annotations"):
                # Create a new DataFrame for the current annotations
                #current_annotations_df = pd.DataFrame(
                    #{'Content': df['Content'][:index], 'Annotation': annotations[:index]})

                # Provide a download link for the current annotations
                #st.markdown(create_download_link(
                    #current_annotations_df, f"{file_name}_current_annotations.csv"), unsafe_allow_html=True)


# Run the app
if __name__ == "__main__":
    main()
