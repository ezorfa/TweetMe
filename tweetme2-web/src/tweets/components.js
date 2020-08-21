import React, {useEffect, useState}  from 'react'

import {apiTweetDetail} from './lookup'
import {Tweet} from './detail'
import {TweetList} from './list'
import {TweetCreate} from './create'


export function TweetComponent(props) {
  const [newTweets, setNewTweets] = useState([])
  const canTweet = props.canTweet === "false" ? false : true
  const handleNewTweet = (newTweet) =>{
    let tempNewTweets = [...newTweets]
    tempNewTweets.unshift(newTweet)
    setNewTweets(tempNewTweets)
  }
  return <div className={props.className}>
          {canTweet === true && <TweetCreate didTweet={handleNewTweet} className='col-12 mb-3' />}
        <TweetList newTweets={newTweets} {...props} />
  </div>
}  

export function TweetDetailComponent(props){

  const {tweetId} = props
  const [didLookup, setDidLookup] = useState(false)
  const [tweet, setTweet] = useState(null)

  const handleTweetLookup = (response, status) => {
    if(status === 200){
      setTweet(response)
    } else {
      alert("There was an error while looking up your tweet :(")
    }
  }

  useEffect(() => {
    if (didLookup === false){
      apiTweetDetail(tweetId, handleTweetLookup)
      setDidLookup(true)
    }
  }, [tweetId, setDidLookup, didLookup])

  return tweet === null ? null : <Tweet tweet={tweet} className={props.className} />
}