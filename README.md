# Jay_KG
&ensp;&ensp;&ensp;&ensp;此项目旨在构建一个关于周杰伦歌曲的知识图谱问答系统。目前知识库本身的内容并不全面，但是麻雀虽小，五脏俱全，该项目对多种类型的问题形式都能得到正确的相应结果。以“晴天”为例，本系统应当能够回答晴天的歌词是什么，晴天是哪首专辑的歌曲，该专辑是哪一年发行的，该专辑对应的歌手是谁，该歌手的的基本信息是什么。关于项目的更多细节在知乎中有更加详细的介绍，知乎网址：https://zhuanlan.zhihu.com/p/58248608<br/><br/>

&ensp;&ensp;&ensp;&ensp;首先，本系统运行在python3环境下，并且需要安装jieba、rerfo等python库，安装方式比较简单，我这里使用pip作为python的包管理工具，直接在cmd中运行pip3 install jieba 即可完成安装。此外，还应当下载apache-jena和apache-jena-fuseki。本系统运行在apache-jena-fuseki服务器上，在cmd窗口进入apache-jena-fuseki文件输入命令./fuseki-server.bat或在文件夹下双击fuseki-server.bat文件，cmd窗口出现“Server  INFO  Started 2019/03/12 21:13:30 CST on port 3030”即表示服务器运行成功，在浏览器输入localhost:3030即可显示页面。<br/><br/>

&ensp;&ensp;&ensp;&ensp;这里apache-jena的主要作用就是使用文件夹中的tdb-loader.bat文件将RDF文件转换成tdb文件，命令格式为：.\tdbloader.bat --loc="D:\tdb" "D:\kg_demo_movie.nt"，--loc参数为生成的tdb文件的文件夹，第二个参数是格式为nt的RDF文件，如果使用protege生成RDF文件，则后缀名为owl，这里可以直接修改文件的后缀名将owl文件转换成nt文件。在D:\apache-jena-fuseki-3.10.0\run\configuration文件下建立fuseki_conf.ttl文件，该文件主要有两个作用，一个是指定tdb文件的位置，另一个是对生成的数据库进行命名，完成转换tdb文件和配置完fuseki_conf.ttl文件后，执行第二段的fuseki-server.bat并打开localhost:3030后应该可以看到服务器上生成的数据库，并可以在该平台上进行SPARQL语句查询。<br/><br/>

&ensp;&ensp;&ensp;&ensp;最后是自然语言处理环节，python通过结巴分词，规则匹配将相应的自然语言转换成SPARQL查询语句，并通过和fuseki通信得到查询结果后通过结果的解析得到最后的答案形式。对于分词等多个文件可以单独的对每个文件的逻辑进行测试，来看懂每个文件所做的工作，也方便debug。<br/><br/>

&ensp;&ensp;&ensp;&ensp;用户可以通过下载apache-jena和apache-jena-fuseki以及github中的fuseki_conf和歌曲知识图谱.owl文件进行测试，注意修改fuseki_conf中的路径。如果是构建自己的知识图谱问答系统，可以在protege中自己写RDF文件，并使用tdb-loader.bat转换成tdb数据。要有一个单独的tdb文件，因为一个owl会生成一堆文件。在构建自己的知识图谱问答系统时，python文件需要更改的部分主要集中在模板匹配并生成相应的SPARQL查询语句环节，其他部分代码大体相同。<br/><br/>

