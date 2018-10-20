# dp_decrypt
## 步骤
> 1. 访问页面
> 2. 通过BeautifulSoup拿到页面svg用的css路径
> 3. 获取并解析css内容,得到code的坐标和svg内容
> 4. 生成code字典
> 5. 获取评论,解析评论中出现的span标签,拿到对应的code,通过3字典取对应的汉字
