import {backendLookup} from '../lookup'

export function apiCreateTweet(newTweet, callback){
    backendLookup("POST", "/tweets/create/", callback, {content: newTweet})
  }

export function apiTweetAction(tweetId, action, callback){
    backendLookup("POST", "/tweets/action/", callback, {id: tweetId , action : action})
}
  
export function apiTweetList(username, callback) {
    let endpoint = '/tweets/'
    if(username){
        endpoint = `/tweets/?username=${username}`
    }
    backendLookup("GET", endpoint, callback)
}

export function apiTweetDetail(tweetId, callback) {
    console.log(tweetId , "tweetId")
    backendLookup("GET", `/tweets/${tweetId}`, callback)
}