import React from 'react';
import ReactDOM from 'react-dom/client';
import {App} from './App';
import {Route, BrowserRouter as Router, Routes} from "react-router-dom";
import {Swap} from "./components/Swap";


ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    <React.StrictMode>

        <Router basename={"/widget"}>

            <Routes>
                <Route path="/" element={<App/>}/>
                <Route path="/swap/*" element={<Swap/>}/>
            </Routes>
        </Router>

    </React.StrictMode>,
);
