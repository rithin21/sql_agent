import React,{useState} from 'react'

export default function Querypage(props) {
    const[prompt,setPrompt] =useState("");
    const[answer,setanswer]=useState(null);
    const[loading,setLoading]=useState(false);



    const submitprompt = async () => {

        setLoading(true);

        try{
            const res = await fetch('http://localhost:8000/run_query',
            {
                method:'POST',
                headers:{
                    'Content-Type':'application/json'
                },
            body:JSON.stringify(
                {
                    "prompt":prompt, 
                    "connectionString": props.ConnectionString
                }
            )   
        })
        const data=await res.json();
        console.log(data);
        setanswer(data);
        }
        catch(err){
            console.log(err);
        }
        finally{
            setLoading(false);
        }
    }
  return (
    <>
        <div className='card-query-page'>
            <h2>Database connection:{props.ConnectionName}</h2>
            <p>Now you can start running your SQL queries and managing your database with ease.</p>
        </div>
        <div className='container mt-5'>
            <div className='d-flex'>
                <input type="text" className='form-control mt-3 ms-3' placeholder='Enter your SQL query here...' onChange={(e)=>setPrompt(e.target.value)} />
                <button className=" btn btn-primary mt-3 ms-3" onClick={()=>{submitprompt()}}>
                    Run Query
                </button>
            </div>
            {
                loading &&
                <div className="mt-3 ms-3">
                    <span className="spinner-border spinner-border-sm"></span>
                    <span className="ms-2">Generating SQL...</span>
                </div>
            }

            {
                answer &&
                <>
                    <h4 className="mt-4 ms-3">
                        Generated SQL
                    </h4>

                    <pre className="bg-light p-3 border rounded ms-3 me-3">
                        {answer.sql_query}
                    </pre>
                </>
            }

            {
                answer &&
                answer.query_result &&
                answer.query_result.length > 0 &&
                (
                    <table className="table table-striped mt-3">

                        <thead>

                            <tr>

                                {
                                    Object.keys(
                                        answer.query_result[0]
                                    ).map((key) => (

                                        <th key={key}>
                                            {key}
                                        </th>

                                    ))
                                }

                            </tr>

                        </thead>

                        <tbody>

                            {
                                answer.query_result.map((row,index)=>(

                                    <tr key={index}>

                                        {
                                            Object.values(row).map(
                                                (value,colIndex)=>(
                                                    <td key={colIndex}>
                                                        {String(value)}
                                                    </td>
                                                )
                                            )
                                        }

                                    </tr>

                                ))
                            }

                        </tbody>

                    </table>
                )
            }
        </div>
    </>
  )
}
