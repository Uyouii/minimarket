-- example HTTP POST script which demonstrates setting the
-- HTTP method, body, and adding a header

wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"

function request()
    user_id = math.random(400)
    user_name=string.format("testuser%d", user_id)
    wrk.body = string.format('{"username":"%s","password":"123456"}', user_name)
    return wrk.format('POST', nil, nil, body)
end