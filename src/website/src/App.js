import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./components/header";
import ToggleOptions from "./components/toggleoptions"
import Dataset from "./components/dataset";
import DoraButtonPage from "./components/dora-button-page";
import NobiButtonPage from "./components/nobi-button-page";
import Images from "./components/images";
import Search from "./components/search";

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
                  <Search/>
                  <ToggleOptions onOptionChange={handleButtonClick}/> {/* sementara aja, harusnya bikin case handle option change */}
                  <Dataset/>
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