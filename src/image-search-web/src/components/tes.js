const Tes = ({ item }) => {
    return [...Array(item).keys()].map(() => (
      <div className="animate-pulse">
        <div className="bg-gray-300 rounded-lg h-30"></div>
      </div>
    ))
  }
  
  export default Tes