window._fs_debug=!1,window._fs_host="fullstory.com",window._fs_org="4NHZM",window._fs_namespace="FS",function(e,o,n,i,s,t,c,a){return n in e&&e.console&&e.console.log?void e.console.log('FullStory namespace conflict. Please set window["_fs_namespace"].'):(c=e[n]=function(e,o){c.q?c.q.push([e,o]):c._api(e,o)},c.q=[],t=o.createElement(i),t.async=1,t.src="https://"+_fs_host+"/s/fs.js",a=o.getElementsByTagName(i)[0],a.parentNode.insertBefore(t,a),c.identify=function(e,o){c(s,{uid:e}),o&&c(s,o)},c.setUserVars=function(e){c(s,e)},c.identifyAccount=function(e,o){t="account",o=o||{},o.acctId=e,c(t,o)},void(c.clearUserCookie=function(e,n,i){if(!e||document.cookie.match("fs_uid=[`;`]*`[`;`]*`[`;`]*`"))for(n=o.domain;;){if(o.cookie="fs_uid=;domain="+n+";path=/;expires="+new Date(0).toUTCString(),i=n.indexOf("."),i<0)break;n=n.slice(i+1)}}))}(window,document,window._fs_namespace,"script","user");