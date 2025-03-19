import express from 'express'

const app = express()

const PORT = 3000

app.use(express.json())

app.listen(PORT, ()=>{
    console.log(`Server running on PORT:${PORT}. We are live.`)
})

app.get('/app',(req,res)=>{
    return res.json({"status":`running on PORT ${PORT}`})
})