import React, { useState, useEffect } from 'react';
import Skeleton from 'react-loading-skeleton';

const Images = () => {
    const [images, setImages] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [currentPage, setCurrentPage] = useState(1);
    const imagesPerPage = 8;

    useEffect(() => {
        const fetchImages = async () => {
            try {
                const response = await fetch('http://localhost:3005/retrieve-images');
                const imageUrls = await response.json();
                const imageObjects = imageUrls.map((path) => ({ url:path }));
                setImages(imageObjects);
            } catch (error) {
                console.error('Error fetching images:', error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchImages();
    }, []);

    const indexOfLastImage = currentPage * imagesPerPage;
    const indexOfFirstImage = indexOfLastImage - imagesPerPage;
    const currentImages = images.slice(indexOfFirstImage, indexOfLastImage);

    const paginate = (pageNumber) => {
        if (pageNumber > 0 && pageNumber <= Math.ceil(images.length / imagesPerPage)) {
            setCurrentPage(pageNumber);
        }
    };

    return (
        <>
            <h1 className="text-center mt-6 text-2xl text-sky-100">Result:</h1>
            <h1 className="text-center text-sky-100">{images.length} results</h1>
            <div className="flex justify-center items-center">
                <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-10 my-10 max-w-7xl mx-auto px-4">
                    {isLoading ? (
                        Array(imagesPerPage).fill(null).map((_, index) => (
                            <Skeleton key={index} height={200} width={'100%'} />
                        ))
                    ) : (
                        currentImages.map((image, index) => (
                            <img
                                key={index}
                                src={image.url}
                                alt=""
                                style={{ width: '80%', height: '100%', objectFit: 'cover' }}
                            />
                        ))
                    )}
                </div>
            </div>
            {/* pagination */}
            <div className='flex justify-center my-4 pb-4'>
                {Array(Math.ceil(images.length / imagesPerPage))
                    .fill(null)
                    .map((_, index) => (
                        <button
                            key={index}
                            onClick={() => paginate(index + 1)}
                            className={`mx-2 p-2 focus:outline-none rounded-full ${currentPage === index + 1 ? 'bg-sky-800 text-white' : 'bg-sky-200 text-sky-700'}`}
                        >
                            {index + 1}
                        </button>
                    ))}
            </div>
        </>
    );
};

export default Images;