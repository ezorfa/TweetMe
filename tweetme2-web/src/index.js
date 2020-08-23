import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
// import App from './App';
import * as serviceWorker from './serviceWorker';
import { FeedComponent, TweetComponent, TweetDetailComponent } from './tweets';
import {ProfileBadgeComponent} from './profiles'

const e = React.createElement
const tweetsEl = document.getElementById('tweetme-2')
if (tweetsEl) {
ReactDOM.render( e(TweetComponent, tweetsEl.dataset), tweetsEl);
}

const eFeed = React.createElement
const tweetFeedEl = document.getElementById('tweetme-2-feed')  // getElementById
if (tweetsEl) {
ReactDOM.render( eFeed(FeedComponent, tweetFeedEl.dataset), tweetFeedEl);
}


const tweetDetailElements = document.querySelectorAll('.tweetme-2-detail')  // querySelectorAll
tweetDetailElements.forEach( container => {
    ReactDOM.render(
        e(TweetDetailComponent, container.dataset), container);
})

const tweetProfileBadgeElements = document.querySelectorAll('.tweetme-2-profile-badge')
tweetProfileBadgeElements.forEach( container => {
    ReactDOM.render(
        e(ProfileBadgeComponent, container.dataset), container);
})

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
