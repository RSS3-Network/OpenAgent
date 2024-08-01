import React from 'react';
import ReactDOM from 'react-dom/client';
import {App, TransferWidgetApp} from './App';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import {Swap} from "./components/Swap";
import {PriceChart} from "./components/PriceChart";
import TransferWidget from "./components/TransferWidget";

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    <React.StrictMode>

        <Router basename={"/widget"}>

            <Routes>
                <Route path="/" element={<App/>}/>
                <Route path="/swap/*" element={<Swap/>}/>
                <Route path="/price-chart/*" element={<PriceChart/>}/>
                 <Route path="/transfer/*" element={
              <TransferWidgetApp>
                <TransferWidget />
              </TransferWidgetApp>
            } />
            </Routes>
        </Router>

    </React.StrictMode>,
);
