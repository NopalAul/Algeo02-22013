import { useContext, useState } from "react";
import { ImageContext } from "../App";
import "./searchfield.css"; // Import your CSS file with the custom styles

const SearchField = () => {
    const [uploadedImage, setUploadedImage] = useState(null);
    const { fetchData, setSearchImage } = useContext(ImageContext);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        setUploadedImage(file);
    }

    const handleUploadAndSearch = () => {
        const formData = new FormData();
        formData.append("image", uploadedImage);

        fetch("/api/upload", {
            method: "POST",
            body: formData,
        })
        .then((response) => response.json())
        .then((data) => {
            fetchData(`search/photos?page=1&query=${data.similarQuery}&client_id=${process.env.REACT_APP_ACCESS_KEY}`);
            setSearchImage(data.similarQuery);
        });
    }

    return (
        <div className="custom-file-input-container">
            <label htmlFor="fileInput" className="custom-file-input">Choose a file</label>
            <input
                type="file"
                id="fileInput"
                style={{ display: "none" }}
                onChange={handleFileChange}
            />
            <button
                onClick={handleUploadAndSearch}
                disabled={!uploadedImage}
                className="upload-search-button"
            >
                Upload & Search
            </button>
        </div>
    );
};

export default SearchField;
