
const getToken = async() =>{
    let token = ''
    try{
        const response = await fetch('http://localhost:8000/token', {
            credentials: 'include'
        })
        if(response.ok) {
            const data = await response.json()
            try {
                token = data.access_token
            }  catch (TypeError){
                token = ''
            }
        }
    } catch(err){
        console.error(err)
    }
    return token
}

export default getToken
