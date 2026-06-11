import React from 'react'
import { useState } from 'react'

export default function Mainpage(props) {

    const[showinput,setShowinput] = useState(false);
    const[connectionString,setConnectionString] = useState("");

    const handleConnect =async () => {
        const res = await fetch('http://localhost:8000/',
            {
                method:'POST',
                headers:{
                    'Content-Type':'application/json'
                },
            body:JSON.stringify({connectionString})   
        })

       
        const data = await res.json();

        if (res.status === 200) {
            props.setConnectionstatus(true);
            console.log(data);
            props.setConnectionName(data.connection_name);
            props.setConnectionURL(connectionString);
        }
    }
    return (
    <>
        <div className='container mt-5'>
            <h1 className="text-center">Welcome to SQL Agent</h1>
            <p className="card-landing-page">SQL Agent is a powerful tool designed to simplify and enhance your database management experience. With SQL Agent, you can easily automate routine tasks, schedule backups, and monitor your database performance with ease. Whether you're a seasoned database administrator or just getting started, SQL Agent provides the tools you need to keep your databases running smoothly and efficiently.</p>
        </div>
        <div className="d-flex flex-column align-items-center mt-4">
            <button className="btn btn-primary" onClick={()=>setShowinput(true)}>
                Connect your database
            </button>
            <div>
                {showinput&&
                <div className='d-flex ms-3'>
                    <input type="text" className='form-control mt-3 ms-3' placeholder='Enter your database connection string here' value={connectionString} onChange={(e) => setConnectionString(e.target.value)} />
                    <button className="btn btn-success mt-3 ms-3" onClick={handleConnect}>
                        Connect
                    </button>
                </div>
                }
            </div>
        </div>
    </>
  )
}

