import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
// import App from './App';
import * as serviceWorker from './serviceWorker';
import { TweetComponent, TweetDetailComponent } from './tweets';

const e = React.createElement
const tweetsEl = document.getElementById('root')

if (tweetsEl) {
ReactDOM.render( e(TweetComponent, tweetsEl.dataset), tweetsEl);
}

const tweetDetailElements = document.querySelectorAll('.tweetme-2-detail')

tweetDetailElements.forEach( container => {
    ReactDOM.render(
        e(TweetDetailComponent, container.dataset), container);
})

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
