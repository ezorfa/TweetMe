import {backendLookup} from '../lookup'

export function apiCreateTweet(newTweet, callback){
    backendLookup("POST", "/tweets/create/", callback, {content: newTweet})
  }

export function apiTweetAction(tweetId, action, callback){
    backendLookup("POST", "/tweets/action/", callback, {id: tweetId , action : action})
}
  
export function apiTweetList(username, callback, nextUrl) {
    let endpoint = '/tweets/'
    if(username){
        endpoint = `/tweets/?username=${username}`
    }
    if (nextUrl !== null && nextUrl !== undefined){
        endpoint = nextUrl.replace("http://localhost:8000/api", "")
    }
    backendLookup("GET", endpoint, callback)
}

export function apiTweetFeed( callback, nextUrl) {
    let endpoint = `/tweets/feed`
    
    if (nextUrl !== null && nextUrl !== undefined){
        endpoint = nextUrl.replace("http://localhost:8000/api", "")
    }
    backendLookup("GET", endpoint, callback)
}

export function apiTweetDetail(tweetId, callback) {
    console.log(tweetId , "tweetId")
    backendLookup("GET", `/tweets/${tweetId}`, callback)
}