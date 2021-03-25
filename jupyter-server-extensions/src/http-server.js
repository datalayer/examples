const http = require('http')

const PORT = 8080

const requestHandler = (request, response) => {
  console.log('URL', request.url)
  console.dir('Params', request.param)
  if (request.method == 'POST') {
    console.log('POST')
    var body = ''
    request.on('data', function(data) {
      body += data
      console.log('Partial body: ' + body)
    })
    request.on('end', function() {
      console.log('Body: ' + body)
      response.setHeader('Content-Type', 'application/json')
      response.end(JSON.stringify({ text: body }))
    })
  } else if (request.method == 'GET') {
    console.log('GET')
    var html = `
            <html>
                <body>
                    <form method="post" action="http://localhost:8080">Name: 
                        <input type="text" name="name" />
                        <input type="submit" value="Submit" />
                    </form>
                </body>
            </html>`
    response.writeHead(200, {'Content-Type': 'text/html'})
    response.end(html)
  }

}

const server = http.createServer(requestHandler)

server.listen(PORT, (err) => {
  if (err) {
    return console.log('something bad happened', err)
  }
  console.log(`HTTP Server is listening on ${PORT}`)
})
