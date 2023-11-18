import React, { useState, useEffect } from 'react';
import Skeleton from 'react-loading-skeleton';
import axios from 'axios';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Images = () => {
    const [images, setImages] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [currentPage, setCurrentPage] = useState(1);
    const imagesPerPage = 10;
    const [imagesLoaded, setImagesLoaded] = useState(false);
    const [data, setData] = useState(null);

    useEffect(() => {
        const fetchImages = async () => {
            try {
                const response = await axios.get('http://localhost:3005/retrieve-images');
                const imageUrls = response.data;
                const imageObjects = imageUrls.map((url) => ({ url }));
                setImages(imageObjects);
            } catch (error) {
                console.error('Error fetching images:', error);
            } finally {
                setIsLoading(false);
                setImagesLoaded(true);
            }
        };

        const fetchData = async () => {
            try {
                const response = await axios.get('http://localhost:3005/durasi');
                const result = response.data;
                setData(result.data);
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchImages();
        fetchData();
    }, []);

    const indexOfLastImage = currentPage * imagesPerPage;
    const indexOfFirstImage = indexOfLastImage - imagesPerPage;
    const currentImages = images.slice(indexOfFirstImage, indexOfLastImage);

    const totalPages = Math.ceil(images.length / imagesPerPage);

    const paginate = (pageNumber) => {
        if (pageNumber > 0 && pageNumber <= totalPages) {
            setCurrentPage(pageNumber);
        }
    };

    const getPageNumbers = () => {
        const pageNumbers = [];
        const maxPagesToShow = 5;

        if (totalPages <= maxPagesToShow) {
            for (let i = 1; i <= totalPages; i++) {
                pageNumbers.push(i);
            }
        } else {
            const halfMaxPagesToShow = Math.floor(maxPagesToShow / 2);
            let startPage = Math.max(1, currentPage - halfMaxPagesToShow);
            let endPage = Math.min(totalPages, startPage + maxPagesToShow - 1);

            if (currentPage <= halfMaxPagesToShow) {
                startPage = 1;
                endPage = maxPagesToShow;
            } else if (currentPage >= totalPages - halfMaxPagesToShow) {
                startPage = totalPages - maxPagesToShow + 1;
                endPage = totalPages;
            }

            if (startPage > 1) {
                pageNumbers.push(1, '...');
            }

            for (let i = startPage; i <= endPage; i++) {
                pageNumbers.push(i);
            }

            if (endPage < totalPages) {
                pageNumbers.push('...', totalPages);
            }
        }

        return pageNumbers;
    };

    const handleHomeRedirect = () => {
        window.location.reload();
      };

    const handleDownloadPDF = async () => {
        try {
            await axios.get('http://localhost:3005/generate-pdf');
            toast.success('PDF generated successfully!', { position: 'top-center', autoClose: 3000 });
        } catch (error) {
            console.error('Error generating PDF:', error);
            toast.error('Error generating PDF. Please try again.', { position: 'top-center', autoClose: 3000 });
        }
    };

    return (
        <>
            <h1 className="text-center mt-6 text-2xl text-sky-100">Result:</h1>
            <h1 className="text-center text-sky-100">{images.length} results</h1>
            <h1 className="text-center text-sky-100">{isLoading ? (
                <p>Loading...</p>
            ) : (
                <p>in {data} seconds</p>
            )}</h1>
            
            <div className="flex justify-center items-center">
                <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-x-10 gap-y-10 my-10 max-w-7xl mx-auto px-4">
                    {isLoading ? (
                        Array(imagesPerPage).fill(null).map((_, index) => (
                            <Skeleton key={index} height={200} width={'100%'} style={{ borderRadius: '10px' }}/>
                        ))
                    ) : (
                        currentImages.map((image, index) => (
                            <div key={index} className="text-center">
                                <img
                                    src={'http://localhost:3005' + image.url}
                                    alt=""
                                    style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '10px' }}
                                />
                                <p className="text-center text-sky-100">{image.url.substring(14, 19) + '%'}</p>
                            </div>
                        ))
                    )}
                </div>
            </div>
            {/* pagination */}
            <div className='flex justify-center my-4 pb-4'>
                {getPageNumbers().map((page, index) => (
                        <button
                            key={index}
                            onClick={() => (typeof page === 'number' ? paginate(page) : null)}
                            className={`mx-2 p-2 focus:outline-none rounded-full ${currentPage === page ? 'bg-sky-800 text-white' : 'bg-sky-200 text-sky-700'}`}
                        >
                            {page}
                        </button>
                    ))}
            </div>
            {/* render button only if images are loaded (try again?) */}
            {imagesLoaded && (
                <div className="flex justify-center my-4 pb-4">
                <button
                    onClick={handleHomeRedirect}
                    className="mx-2 p-2 focus:outline-none rounded-full bg-sky-200 text-sky-700 try-again-button"
                >
                    Try again?
                </button>
                <button
                    onClick={handleDownloadPDF}
                    className="mx-2 p-2 focus:outline-none rounded-full bg-sky-200 text-sky-700 try-again-button"
                >
                    Download Result as PDF
                </button>
                </div>
            )}
        </>
    );
};

export default Images;