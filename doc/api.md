[toc]

### 用户注册

url: `/auth/register/`

method: ` post`

request:

```json
{
  "username": "taiyou.dong",
  "password": "123456", 
  "avatar": "https://lh3.googleusercontent.com/a-/AOh14GgwkYXAa-1SMCDRpgsmIQfs8vH-VBqxkGla11pK\\=s192-c-mo"
}
```

response:

```json
{
  "username": "taiyou.dong",
  "user_id": 1900307088242182,
  "errcode": 0
}
```

请求示例：

```sh
curl -d '{"username": "taiyou.dong", "password": "123456", "avatar": "https://lh3.googleusercontent.com/a-/AOh14GgwkYXAa-1SMCDRpgsmIQfs8vH-VBqxkGla11pK\\=s192-c-mo"}' 'http://127.0.0.1:8000/auth/register/'
```

### 用户登录

url : `/auth/login/`

method: `post`

request:

```json
{
  "username": "taiyou.dong", 
  "password": "123456"
}
```

response:

```json
{
  "session": "80b8fa21dbd458c758579d19",
  "user_id": 1900307088242182,
  "errcode": 0,
  "logintime": 1650014061
}
```

请求示例：

```sh
curl -d '{"username": "taiyou.dong", "password": "123456"}' 'http://127.0.0.1:8000/auth/login/'
```

### 通过商品id获取商品详情

url: `/product/id/[productid]`

method: `post`

request：

```json
{
  "session": "afa8a717e3dbfec56312d86e", 
  "user_id": 1900307088242182
}
```

response:

```json
{
  "product_data": {
    "photo": "https://cf.shopee.sg/file/f262efa8b24f6d9c67ada8a5062ed4d2",
    "descript": "iPhone 13. The most advanced dual-camera system ever on iPhone. Lightning-fast A15 Bionic chip. A big leap in battery life. Durable design. Super-fast 5G.1 And a brighter Super Retina XDR display.",
    "cate": "Mobile Phones & Tablets",
    "name": "Apple iPhone 13",
    "id": 101
  },
  "errcode": 0
}
```

请求示例：

```sh
curl -d '{"session": "afa8a717e3dbfec56312d86e", "user_id": 1900307088242182}' 'http://127.0.0.1:8000/product/id/101/'
```

### 获取所有商品

url: `/product/all/`

method:  `post`

request:

```json
{
  "cur_page": "1", 
  "session": "806592c32a12b55368972cd1", 
  "user_id": 1900307088242182, 
  "page_size": "3"
}
```

response:

```json
{
  "product_list": [
    {
      "photo": "https://cf.shopee.sg/file/d7de31b23d8302a215b120f4048c9049",
      "cate": "Fine Jewellery",
      "name": "Goldheart Perol\u00e9 Pearl 14K White Gold Necklace",
      "id": 103
    },
    {
      "photo": "https://cf.shopee.sg/file/5765229fe1a361fdc5d72fc3e4d8bc7a",
      "cate": "Dresses",
      "name": "Online Exclusive Embroidery F-box Logo Back Slit Cotton Dress",
      "id": 104
    },
    {
      "photo": "https://cf.shopee.sg/file/28331eee43756d81ff2a6ad2e0c0d415",
      "cate": "Sweaters & Cardigans",
      "name": "New Spot Large Size M-3XL Japanese Naruto Print Hoodie Sweater Hoodie Hooded Sweater Couple",
      "id": 105
    }
  ],
  "errcode": 0
}
```

请求示例：

```sh
curl -d '{"cur_page": "1", "session": "806592c32a12b55368972cd1", "user_id": 1900307088242182, "page_size": "3"}' 'http://127.0.0.1:8000/product/all/'
```

### 根据名称搜索商品

url: `/product/searchname/`

method:  `post`

request:

```json
{
  "cur_page": "0", 
  "session": "5b933fc414e39e62b05b1030", 
  "user_id": 1900307088242182, 
  "name": "iphon", 
  "page_size": "5"
}
```

response:

```json
{
  "product_list": [
    {
      "photo": "https://cf.shopee.sg/file/f262efa8b24f6d9c67ada8a5062ed4d2",
      "cate": "Mobile Phones & Tablets",
      "name": "Apple iPhone 13",
      "id": 101
    }
  ],
  "errcode": 0
}
```

请求示例：

```sh
curl -d '{"cur_page": "0", "session": "5b933fc414e39e62b05b1030", "user_id": 1900307088242182, "name": "iphon", "page_size": "5"}' 'http://127.0.0.1:8000/product/searchname/'
```



### 根据类目搜索商品

url: `/product/searchcate/'`

method:  `post`

request:

```json
{
  "cur_page": "0", 
  "session": "118cf013062d7b0bb7d2183d", 
  "user_id": 1900307088242182, 
  "cate": "phon", 
  "page_size": "5"
}
```

response:

```json
{
  "product_list": [
    {
      "photo": "https://cf.shopee.sg/file/f262efa8b24f6d9c67ada8a5062ed4d2",
      "cate": "Mobile Phones & Tablets",
      "name": "Apple iPhone 13",
      "id": 101
    }
  ],
  "errcode": 0
}
```

请求示例：

```sh
curl -d '{"cur_page": "0", "session": "118cf013062d7b0bb7d2183d", "user_id": 1900307088242182, "cate": "phon", "page_size": "5"}' 'http://127.0.0.1:8000/product/searchcate/'
```

### 根据ID拉取评论详情

url: `/comment/id/[id]/`

method:  `post`

request:

```json
{
  "session": "490cf28f4af37c7b47e85636", 
  "user_id": 1900307088242182
}
```

response:

```json
{
  "errcode": 0,
  "comment_data": {
    "user_id": 1507301223750153,
    "product_id": 100,
    "img": "",
    "content": "it's ugly but useful",
    "create_time": 1650012712085,
    "id": 394104924953088
  }
}
```

请求示例：

```sh
curl -d '{"session": "490cf28f4af37c7b47e85636", "user_id": 1900307088242182}' 'http://127.0.0.1:8000/comment/id/394104924953088/'
```



### 添加商品评论

url: `/comment/addcomment/`

method:  `post`

request:

```json
{
  "user_id": 1900307088242182, 
  "product_id": 101, 
  "img": "", 
  "resp_comment_id": 0, 
  "content": "test add a comment", 
  "session": "95e625d570b396e6f76bf42c"
}
```

response:

```json
{
  "errcode": 0,
  "comment_data": {
    "user_id": 1900307088242182,
    "product_id": 101,
    "img": "",
    "content": "test add a comment",
    "create_time": 1650015666338,
    "id": 406495959678209
  }
}
```

请求示例：

```sh
curl -d '{"user_id": 1900307088242182, "product_id": 101, "img": "", "resp_comment_id": 0, "content": "test add a comment", "session": "95e625d570b396e6f76bf42c"}' 'http://127.0.0.1:8000/comment/addcomment/'
```



### 回复商品评论

url: `/comment/responsecomment/`

method:  `post`

request:

```json
{
  "content": "you are right", 
  "session": "a2864b11e1840c9c46a8ee0a", 
  "user_id": 1900307088242182, 
  "img": "", 
  "resp_comment_id": 406495959678209
}
```

response:

```json
{
  "errcode": 0,
  "comment_data": {
    "user_id": 1900307088242182,
    "product_id": 101,
    "img": "",
    "content": "you are right",
    "create_time": 1650015822506,
    "id": 407150976286977
  }
}
```

请求示例：

```sh
curl -d '{"content": "you are right", "session": "a2864b11e1840c9c46a8ee0a", "user_id": 1900307088242182, "img": "", "resp_comment_id": 406495959678209}' 'http://127.0.0.1:8000/comment/responsecomment/'
```

### 获取商品的评论

url: `/comment/productcomments/`

method:  `post`

request:

```json
{
  "cur_page": "1", 
  "session": "ddc076a021d711dfa029a041", 
  "user_id": 1900307088242182, 
  "product_id": 100, 
  "page_size": "3"
}
```

response:

```json
{
  "comment_list": [
    {
      "content": "how to use it",
      "create_time": 1650012716066,
      "user_id": 1514332880696832,
      "id": 394121622426752,
      "img": ""
    },
    {
      "content": "I like it very much",
      "create_time": 1650012716048,
      "user_id": 1514332880696832,
      "id": 394121546853888,
      "img": ""
    },
    {
      "content": "The serum smells good. Delivery was also prompt. Item received in good condition.",
      "create_time": 1650012716026,
      "user_id": 1514332880696832,
      "id": 394121454011776,
      "img": ""
    }
  ],
  "errcode": 0
}
```

请求示例：

```sh
curl -d '{"cur_page": "1", "session": "ddc076a021d711dfa029a041", "user_id": 1900307088242182, "product_id": 100, "page_size": "3"}' 'http://127.0.0.1:8000/comment/productcomments/'
```

### 获取评论的回复

url: `/comment/commentresponses/`

method:  `post`

request:

```json
{
  "cur_page": "0", 
  "comment_id": 394136420728192, 
  "session": "703f0c1a468661d72af08dd8", 
  "user_id": 1900307088242182, 
  "page_size": "5"
}
```

response:

```json
{
  "comment_list": [
    {
      "content": "= =",
      "create_time": 1650012836008,
      "user_id": 1507260750133120,
      "id": 394624696458112,
      "img": ""
    },
    {
      "content": "wrong !",
      "create_time": 1650012819954,
      "user_id": 1507260750133120,
      "id": 394557357207424,
      "img": ""
    }
  ],
  "errcode": 0
}
```

请求示例：

```sh
curl -d '{"cur_page": "0", "comment_id": 394136420728192, "session": "703f0c1a468661d72af08dd8", "user_id": 1900307088242182, "page_size": "5"}' 'http://127.0.0.1:8000/comment/commentresponses/'
```

