(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-4572"],{CyXH:function(t,e,n){"use strict";n.r(e);var i=n("ytsJ"),r=n("t3Un");var s=n("Mj6V"),a=n.n(s),o=(n("pdi6"),{name:"Crawler",data:function(){return{weixins:[{nickname:"拼命牵手WCplus中...",nick_name:"稍等几秒钟...",reading:"0",more:"0"}],filter:{type:!0,num:"",num_range:[{label:"最近10篇",value:"10"},{label:"最近100篇",value:"100"},{label:"最近1000篇",value:"1000"},{label:"最近5000篇",value:"5000"},{label:"全部历史",value:"0"}],range:25,article_location:0,time_gap:"",time_picker_options:{shortcuts:[{text:"最近一周",onClick:function(t){var e=new Date,n=new Date;n.setTime(n.getTime()-6048e5),t.$emit("pick",[n,e])}},{text:"最近一个月",onClick:function(t){var e=new Date,n=new Date;n.setTime(n.getTime()-2592e6),t.$emit("pick",[n,e])}},{text:"最近三个月",onClick:function(t){var e=new Date,n=new Date;n.setTime(n.getTime()-7776e6),t.$emit("pick",[n,e])}},{text:"最近半年",onClick:function(t){var e=new Date,n=new Date;n.setTime(n.getTime()-15552e6),t.$emit("pick",[n,e])}},{text:"最近一年",onClick:function(t){var e=new Date,n=new Date;n.setTime(n.getTime()-31536e6),t.$emit("pick",[n,e])}}]}},pause:0,progress:{busy:0,current:1,steps:[{title:"暂无搜集步骤",des:"添加搜集任务后 此处将显示搜集进度",percent:100,color:"#ff000"}]}}},created:function(){a.a.start(),this.$socket.emit("ask_data","req_data"),a.a.done()},methods:{currentProcess:function(t){return this.progress.busy?t-1:t},format_timestamp:function(t){return Object(i.timestampFormat)(t)},formatTooltip:function(){return 0===this.filter.range?"仅搜集文章列表":25===this.filter.range?"文章列表+正文内容":50===this.filter.range?"文章列表+阅读数据":75===this.filter.range?"文章列表+正文内容+阅读数据":100===this.filter.range?"仅阅读数据":void 0},formatArticleLocation:function(){var t=["仅头条","加次1","加次2","加次3","加次4","加次5","加次6","全部"];return this.filter.article_location<=70?t[this.filter.article_location/10]:t[7]},begin2Crawl:function(){var t=this,e={range:this.filter.range,type:this.filter.type,num:this.filter.num,start_time:this.filter.time_gap[0],end_time:this.filter.time_gap[1],article_location:this.filter.article_location};if(0!==this.weixins.length||e.num){var n=this,i=!1;if(this.weixins.forEach(function(t){"?"===t.nick_name&&(console.log(t),n.$message({message:"需要点击该公众号的具体文章消除问号?",type:"warning"}),i=!0),"UNK"===t.nickname&&(console.log(t),n.$message({message:"需要点击公众号的全部消息来获得文章列表",type:"warning"}),i=!0),"0"===t.reading&&(console.log(t),n.$message({message:"请先点击该公众号的任意一一篇文章 直到时间显示刚刚",type:"warning"}),i=!0),"0"===t.more&&(console.log(t),n.$message({message:"请先上滑公众号加载更多历史消息 直到时间显示刚刚",type:"warning"}),i=!0)}),!i){if(console.log(this.weixins),e.type){if(!e.num)return void this.$message({message:"按数量搜集 需要选定搜集数量",type:"error"})}else if(!this.filter.time_gap)return void this.$message({message:"按时间搜集 需要选定时间区间",type:"error"});this.$alert("搜集的过程中不要使用参加搜集的微信浏览其余微信公众号文章或历史文章列表 如需此操作 请先断开手机代理","注意",{confirmButtonText:"确定",callback:function(n){t.$message({message:"搜集任务添加成功",type:"success"}),function(t){Object(r.a)({url:"/crawler",method:"post",params:t})}(e)}})}}else this.$alert({message:"请先设置代理并操作微信来获取参数",type:"error"})},deleteWeixin:function(t){for(var e=0;e<this.weixins.length;e++)t===this.weixins[e].nick_name&&this.weixins.pop(e);!function(t){Object(r.a)({url:"/crawler",method:"delete",params:t})}({nick_name:t})},handlerPause:function(){this.pause=!this.pause,this.$socket.emit("pause",this.pause),this.$message({message:"暂停/恢复搜集",type:"success"})}},socket:{events:{req_data:function(t){this.weixins=t},process:function(t){this.progress=t},pause:function(t){this.pause=!0}}}}),l=(n("Ffy0"),n("KHd+")),c=Object(l.a)(o,function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"app-container unselectable"},[n("div",{staticClass:"w3-padding w3-border w3-round-large",staticStyle:{"margin-bottom":"20px","margin-left":"10px","margin-right":"10px",background:"rgba(0,0,0,0.04)","min-width":"360px"}},[n("el-steps",{attrs:{active:t.currentProcess(t.progress.current),"finish-status":"success","align-center":""}},t._l(t.progress.steps,function(t){return n("el-step",{key:t.title,attrs:{title:t.title,description:t.des}})}))],1),t._v(" "),n("el-progress",{staticStyle:{"margin-bottom":"20px","margin-left":"10px","margin-right":"10px","min-width":"360px"},attrs:{"text-inside":!0,"stroke-width":18,percentage:t.progress.steps[t.progress.current-1].percent}}),t._v(" "),t._l(t.weixins,function(e){return n("div",{key:e.nick_name,staticClass:"w3-round w3-card-4 weixin"},[n("header",{staticClass:"w3-container w3-round w3-green"},[n("h5",{staticStyle:{float:"left"}},[n("i",{staticClass:"fa fa-wechat"}),t._v(" "+t._s(e.nick_name))]),t._v(" "),n("el-tooltip",{staticStyle:{"margin-top":"10px",float:"right"},attrs:{content:"慎重 单击删除微信参数"}},[n("el-button",{staticClass:"w3-red",attrs:{size:"mini",icon:"el-icon-delete",circle:""},on:{click:function(n){t.deleteWeixin(e.nick_name)}}})],1)],1),t._v(" "),n("div",{staticClass:"w3-container"},[n("p",[t._v("公众号 : "+t._s(e.nickname))]),t._v(" "),n("p",[t._v("历史消息: "+t._s(t.format_timestamp(e.more)))]),t._v(" "),n("p",[t._v("阅读数据: "+t._s(t.format_timestamp(e.reading)))])])])}),t._v(" "),n("div",{staticClass:"w3-round w3-card-4 weixin"},[t._m(0),t._v(" "),n("div",{staticClass:"w3-container"},[n("el-row",[n("el-col",{attrs:{span:12}},[n("div",{staticClass:"grid-content bg-purple"},[n("el-switch",{staticStyle:{display:"block","margin-top":"10px"},attrs:{align:"left","active-color":"#13ce66","inactive-color":"#ff3939","active-text":"数量","inactive-text":"时间"},model:{value:t.filter.type,callback:function(e){t.$set(t.filter,"type",e)},expression:"filter.type"}})],1)]),t._v(" "),n("el-col",{attrs:{span:12}},[n("div",{staticClass:"grid-content bg-purple-light"},[n("el-slider",{staticStyle:{"margin-top":"3px"},attrs:{"format-tooltip":t.formatTooltip,step:25,"show-stops":"","show-stop":""},model:{value:t.filter.range,callback:function(e){t.$set(t.filter,"range",e)},expression:"filter.range"}})],1)])],1),t._v(" "),t.filter.type?n("el-select",{staticStyle:{"margin-top":"10px",width:"100%"},attrs:{size:"small",placeholder:"请选择搜集数量"},model:{value:t.filter.num,callback:function(e){t.$set(t.filter,"num",e)},expression:"filter.num"}},t._l(t.filter.num_range,function(t){return n("el-option",{key:t.value,attrs:{label:t.label,value:t.value}})})):n("el-date-picker",{staticStyle:{"margin-top":"10px",width:"100%"},attrs:{"picker-options":t.filter.time_picker_options,type:"daterange",align:"right",size:"small","unlink-panels":"","range-separator":"-","start-placeholder":"开始","end-placeholder":"结束"},model:{value:t.filter.time_gap,callback:function(e){t.$set(t.filter,"time_gap",e)},expression:"filter.time_gap"}}),t._v(" "),n("el-row",{attrs:{gutter:10}},[n("el-col",{attrs:{span:12}},[t.progress.busy?n("el-button",{staticStyle:{"margin-top":"10px",width:"100%"},attrs:{loading:!0,type:"default",size:"small"},on:{click:function(e){t.begin2Crawl()}}},[t._v("正在搜集")]):n("el-button",{staticStyle:{"margin-top":"10px",width:"100%"},attrs:{type:"success",size:"small"},on:{click:function(e){t.begin2Crawl()}}},[t._v("开始搜集")])],1),t._v(" "),n("el-col",{attrs:{span:12}},[n("el-button",{staticStyle:{"margin-top":"10px",width:"100%"},attrs:{type:"warning",size:"small"},on:{click:function(e){t.handlerPause()}}},[t._v("启动/暂停")])],1)],1)],1)]),t._v(" "),t.filter.range>=50?n("div",{staticClass:"w3-round w3-card-4 weixin"},[t._m(1),t._v(" "),n("div",{staticClass:"w3-container"},[n("el-row",[n("div",{staticClass:"grid-content bg-purple-light"},[n("el-slider",{staticStyle:{"margin-top":"3px"},attrs:{"format-tooltip":t.formatArticleLocation,step:10,"show-stops":"","show-stop":""},model:{value:t.filter.article_location,callback:function(e){t.$set(t.filter,"article_location",e)},expression:"filter.article_location"}})],1)]),t._v(" "),n("el-row",[n("p",[t._v(t._s(t.formatArticleLocation())+" 文章的阅读数据")]),t._v(" "),n("p",[t._v("10表示头条 11表示次1 以此类推")])])],1)]):t._e()],2)},[function(){var t=this.$createElement,e=this._self._c||t;return e("header",{staticClass:"w3-container w3-round w3-blue"},[e("h5",[e("i",{staticClass:"fa fa-bug"}),this._v(" 搜集")])])},function(){var t=this.$createElement,e=this._self._c||t;return e("header",{staticClass:"w3-container w3-round w3-red"},[e("p",[e("i",{staticClass:"fa fa-list"}),this._v(" 哪些文章需要阅读数据？越靠左搜集越快")])])}],!1,null,"5556d3c0",null);c.options.__file="crawler.vue";e.default=c.exports},Ffy0:function(t,e,n){"use strict";var i=n("OqqT");n.n(i).a},Mj6V:function(t,e,n){var i,r;
/* NProgress, (c) 2013, 2014 Rico Sta. Cruz - http://ricostacruz.com/nprogress
 * @license MIT */void 0===(r="function"==typeof(i=function(){var t={version:"0.2.0"},e=t.settings={minimum:.08,easing:"ease",positionUsing:"",speed:200,trickle:!0,trickleRate:.02,trickleSpeed:800,showSpinner:!0,barSelector:'[role="bar"]',spinnerSelector:'[role="spinner"]',parent:"body",template:'<div class="bar" role="bar"><div class="peg"></div></div><div class="spinner" role="spinner"><div class="spinner-icon"></div></div>'};function n(t,e,n){return t<e?e:t>n?n:t}function i(t){return 100*(-1+t)}t.configure=function(t){var n,i;for(n in t)void 0!==(i=t[n])&&t.hasOwnProperty(n)&&(e[n]=i);return this},t.status=null,t.set=function(a){var o=t.isStarted();a=n(a,e.minimum,1),t.status=1===a?null:a;var l=t.render(!o),c=l.querySelector(e.barSelector),u=e.speed,p=e.easing;return l.offsetWidth,r(function(n){""===e.positionUsing&&(e.positionUsing=t.getPositioningCSS()),s(c,function(t,n,r){var s;return(s="translate3d"===e.positionUsing?{transform:"translate3d("+i(t)+"%,0,0)"}:"translate"===e.positionUsing?{transform:"translate("+i(t)+"%,0)"}:{"margin-left":i(t)+"%"}).transition="all "+n+"ms "+r,s}(a,u,p)),1===a?(s(l,{transition:"none",opacity:1}),l.offsetWidth,setTimeout(function(){s(l,{transition:"all "+u+"ms linear",opacity:0}),setTimeout(function(){t.remove(),n()},u)},u)):setTimeout(n,u)}),this},t.isStarted=function(){return"number"==typeof t.status},t.start=function(){t.status||t.set(0);var n=function(){setTimeout(function(){t.status&&(t.trickle(),n())},e.trickleSpeed)};return e.trickle&&n(),this},t.done=function(e){return e||t.status?t.inc(.3+.5*Math.random()).set(1):this},t.inc=function(e){var i=t.status;return i?("number"!=typeof e&&(e=(1-i)*n(Math.random()*i,.1,.95)),i=n(i+e,0,.994),t.set(i)):t.start()},t.trickle=function(){return t.inc(Math.random()*e.trickleRate)},function(){var e=0,n=0;t.promise=function(i){return i&&"resolved"!==i.state()?(0===n&&t.start(),e++,n++,i.always(function(){0==--n?(e=0,t.done()):t.set((e-n)/e)}),this):this}}(),t.render=function(n){if(t.isRendered())return document.getElementById("nprogress");o(document.documentElement,"nprogress-busy");var r=document.createElement("div");r.id="nprogress",r.innerHTML=e.template;var a,l=r.querySelector(e.barSelector),c=n?"-100":i(t.status||0),p=document.querySelector(e.parent);return s(l,{transition:"all 0 linear",transform:"translate3d("+c+"%,0,0)"}),e.showSpinner||(a=r.querySelector(e.spinnerSelector))&&u(a),p!=document.body&&o(p,"nprogress-custom-parent"),p.appendChild(r),r},t.remove=function(){l(document.documentElement,"nprogress-busy"),l(document.querySelector(e.parent),"nprogress-custom-parent");var t=document.getElementById("nprogress");t&&u(t)},t.isRendered=function(){return!!document.getElementById("nprogress")},t.getPositioningCSS=function(){var t=document.body.style,e="WebkitTransform"in t?"Webkit":"MozTransform"in t?"Moz":"msTransform"in t?"ms":"OTransform"in t?"O":"";return e+"Perspective"in t?"translate3d":e+"Transform"in t?"translate":"margin"};var r=function(){var t=[];function e(){var n=t.shift();n&&n(e)}return function(n){t.push(n),1==t.length&&e()}}(),s=function(){var t=["Webkit","O","Moz","ms"],e={};function n(n){return n=function(t){return t.replace(/^-ms-/,"ms-").replace(/-([\da-z])/gi,function(t,e){return e.toUpperCase()})}(n),e[n]||(e[n]=function(e){var n=document.body.style;if(e in n)return e;for(var i,r=t.length,s=e.charAt(0).toUpperCase()+e.slice(1);r--;)if((i=t[r]+s)in n)return i;return e}(n))}function i(t,e,i){e=n(e),t.style[e]=i}return function(t,e){var n,r,s=arguments;if(2==s.length)for(n in e)void 0!==(r=e[n])&&e.hasOwnProperty(n)&&i(t,n,r);else i(t,s[1],s[2])}}();function a(t,e){var n="string"==typeof t?t:c(t);return n.indexOf(" "+e+" ")>=0}function o(t,e){var n=c(t),i=n+e;a(n,e)||(t.className=i.substring(1))}function l(t,e){var n,i=c(t);a(t,e)&&(n=i.replace(" "+e+" "," "),t.className=n.substring(1,n.length-1))}function c(t){return(" "+(t.className||"")+" ").replace(/\s+/gi," ")}function u(t){t&&t.parentNode&&t.parentNode.removeChild(t)}return t})?i.call(e,n,e,t):i)||(t.exports=r)},OqqT:function(t,e,n){},pdi6:function(t,e,n){},t3Un:function(t,e,n){"use strict";var i=n("vDqi"),r=n.n(i).a.create({baseURL:"http://localhost:5000/api",timeout:5e3});e.a=r},ytsJ:function(t,e){t.exports={timestampFormat:function(t){function e(t){return(1===String(t).length?"0":"")+t}var n=parseInt((new Date).getTime()/1e3),i=n-t,r=new Date(1e3*n),s=new Date(1e3*t),a=s.getFullYear(),o=s.getMonth()+1,l=s.getDate(),c=s.getHours(),u=s.getMinutes();if(i<60)return"刚刚";if(i<3600)return Math.floor(i/60)+"分钟前";if(r.getFullYear()===a&&r.getMonth()+1===o&&r.getDate()===l)return"今天"+e(c)+":"+e(u);var p=new Date(1e3*(n-86400));return p.getFullYear()===a&&p.getMonth()+1===o&&p.getDate()===l?"昨天"+e(c)+":"+e(u):r.getFullYear()===a?e(o)+"月"+e(l)+"日 "+e(c)+":"+e(u):a+"年"+e(o)+"月"+e(l)+"日 "+e(c)+":"+e(u)}}}}]);