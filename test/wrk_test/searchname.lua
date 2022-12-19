-- example HTTP POST script which demonstrates setting the
-- HTTP method, body, and adding a header

wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"

function request()
    cur_page = math.random(100)
    wrk.body = string.format(
        '{"user_id":1507260750133120,"session":"74e805a753e12507c71be2d5","page_size":5,"name":"apple","cur_page":%d}', cur_page)
    return wrk.format('POST', nil, nil, body)
end