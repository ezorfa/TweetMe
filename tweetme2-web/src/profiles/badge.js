import React, {useEffect, useState} from 'react'

import {apiProfileDetail, apiProfileFollowToggle} from './lookup'

import {UserDisplay, UserPicture} from './components'

export function ProfileBadge (props) {
  console.log("ProfileBadge***")
  const {user, didFollowToggle} = props
  const currentVerb = (user && user.is_following) ? "Unfollow" : "Follow"
  console.log(currentVerb)
  const handleFollowToggle = (event) => {
    console.log("handleFollowToggle")
    // event.preventDefault()
    if (didFollowToggle) {
      console.log(currentVerb, "handleFollowToggle")
      didFollowToggle(currentVerb)
    }   
  }  
  return user ? 
                <div> 
                  <UserPicture user={user} hideLink/> 
                  <p>
                    <UserDisplay user={user} includeFullName hideLink /></p> 
<button className='btn btn-primary' onClick={handleFollowToggle}>{currentVerb}</button>
                </div>
                
                                                              : null
}

export function ProfileBadgeComponent (props) {
    const {username} = props
    // lookup
    const [didLookup, setDidLookup] = useState(false)
    const [profile, setProfile] = useState(null)
    const handleBackendLookup = (response, status) => {
      if (status === 200) {
        console.log(response, "handleBackendLookup")
        setProfile(response)
      }
    }
    useEffect(()=>{
      console.log( "useEffect")
      if (didLookup === false ){
        apiProfileDetail(username, handleBackendLookup)
        setDidLookup(true)
      }
    }, [username, didLookup, setDidLookup])

    const handleNewFollow = (actionVerb) => {
      apiProfileFollowToggle(username, actionVerb, (response, status) => {
        console.log(response, status, "handleNewFollow")
        if (status === 200){
          setProfile(response)
        }
      })
    }

    return didLookup === false ? "Loading..." : profile ? <ProfileBadge user={profile} didFollowToggle={handleNewFollow} /> : null
}