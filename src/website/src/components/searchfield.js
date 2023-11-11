import "./search-field.css";

const SearchField = () => {
    return (
        <div className="custom-file-input-container flex items-center">
            <label htmlFor="fileInput" className="custom-file-input" style={{ fontFamily: 'Comic Sans MS, cursive'}}>Choose a file</label>
            <input
                type="file"
                id="fileInput"
                style={{ display: "none" }}
            />
            <button
                className="upload-search-button"
                style={{ fontFamily: 'Comic Sans MS, cursive'}}>
                Upload & Search
            </button>
        </div>
    );
};

export default SearchField;
