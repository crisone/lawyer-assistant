# Lawyer-Assistant

## 抓取文档思路

1. 通过浏览器调试工具，找到搜索请求的方法
2. 模拟搜索请求，得到对应的结果页面

## 运行测试

```
python spider.py
```


## 简单解释

```
s = UNSpider() # 新建对象
s.init_cookies() # 初始化

fp = s.init_search("non-intervention") # 初始化搜索，如果成功的话返回搜索第一页 的 html

p3 = s.get_search_page(3) # 获得第三页搜索结果 的 html
```
