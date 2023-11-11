import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./components/header";
import SearchField from "./components/searchfield";
import DoraButtonPage from "./components/dora-button-page";
import NobiButtonPage from "./components/nobi-button-page";
import Images from "./components/images";

function App() {
  const handleButtonClick = () => {
    console.log('Button clicked');
  }

  return (
    <Router>
        <Routes>
          <Route 
            path="/" 
            element={
              <div>
                <Header onButtonClick={handleButtonClick}>
                  <SearchField/>
              </Header>
              <Images/>
            </div> }>
          </Route>
          <Route path="/buttonpage" element={<DoraButtonPage />} />
          <Route path="/nobi-button-page" element={<NobiButtonPage />} />
        </Routes>
    </Router>
  );
}

export default App;