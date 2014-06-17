crawler.py
==========
It is designed to function as a basic crawler not too much complicated at the start (as I don't want to finish the book at the first page nor I can't).

[ Background ]
I was always amused by amount of data which is one the web and how beautifully and simply Google make it more organised, understandable and access with in a single page. I always use to think about it how Google do such thing. So in order to understand it I decided to do it myself.
 In my journey to build something useful I will start from the crawler which not too complicated. It have to some basic task such as creating snapshot of the pages on GFS [1] for future analysis and keep updating the file which use to change w.r.t. There will be different types Digester (aka Information Retrieval Module) which will analyse the content and produce the information out it.  For example, 1- “Image Analyser” will process each image and will produce the colour histogram of it which will be used to in Image Search. It is not the best way we will improve it. 2- “Site Analyser” will render different site and figure out the layout and filter out the common element which appears it will help in getting the actual content of a page.  And many more…


[1] GFS (Global File System): It will store the file along with additional details such that it can be accessed by URI and more than one version of same file can be stored and managed.
