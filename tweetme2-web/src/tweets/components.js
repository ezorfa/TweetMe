  
import React, {useEffect, useState}  from 'react'

import {loadTweets} from '../lookup'

export function TweetComponent(props){
  const textAreaRef = React.createRef()
  const handleSubmit = (event) => {
    event.preventDefault()
    console.log(event)
    console.log(textAreaRef.current.value)
    textAreaRef.current.value = ''
  }
  
  return <div className={props.className}>
    <div className='col-12'>
    <form onSubmit={handleSubmit}>
    <textarea ref={textAreaRef} required={true} className='form-control' name='tweet'>
 
    </textarea>
    <button type='submit' className='btn btn-primary my-3'>Tweet</button>
  </form>
  </div>
  <TweetList/>
  </div>
}

export function ActionBtn(props) {
    const {tweet, action} = props
    const [tweetLikes, setTweetLikes] = useState(tweet.likes ? tweet.likes : 0)
    const [justClicked, setJustClicked] = useState(false)
    const className = props.className ? props.className : 'btn btn-primary btn-sm'
    const actionDisplay = action.display ? action.display : 'Action'
    const handleClick = (event) => {
      event.preventDefault()
      if (action.type === 'like') {
        if (justClicked === true){
           setJustClicked(false)
           setTweetLikes(tweetLikes - 1 )
        }
        else { 
          setJustClicked(true)
          setTweetLikes(tweet.likes + 1)
        }
      }
    }
    const display = action.type === 'like' ? `${tweetLikes} ${actionDisplay}` : actionDisplay
    return <button className={className} onClick={handleClick}>{display}</button>
  }
  
export function Tweet(props) {  
    const {tweet}  = props
    const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
    return <div className= {className}>
        <p>{tweet.id} - {tweet.content}</p>
        <div className='btn btn-group'>
        <ActionBtn tweet={tweet} action={{type : "like" , display : "Likes"}}/>
        <ActionBtn tweet={tweet} action={{type : "unlike" , display : "Unlike"}}/>
        <ActionBtn tweet={tweet} action={{type : "retweet" , display : ""}}/>
        </div>
    </div>
}

export function TweetList(props){
    const [tweets, setTweets] = useState([])
 
    useEffect(() => {
      const myCallback = (response, status) => {
        if (status === 200){
          setTweets(response)
        } else {
          alert("There was an error")
        }
      }
      loadTweets(myCallback)
    }, [])

    return <div>
      {tweets.map( (item, index) => {
        return <Tweet tweet={item} className='my-5 py-5 border bg-white text-dark' key={`${index} - ${item.id}`} />
      })}
      </div>
  }