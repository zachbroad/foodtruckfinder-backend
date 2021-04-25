!function(){"use strict";var e={45585:function(e,t,n){var r=this&&this.__importDefault||function(e){return e&&e.__esModule?e:{default:e}};t.__esModule=!0;var o=r(n(73609));window.createPageChooser=function(e,t,n){var r=o.default("#"+e+"-chooser"),a=r.find(".title"),u=o.default("#"+e),i=r.find(".edit-link"),l=r.data("chooserUrl"),c=null;u.val()&&(c={id:u.val(),parentId:t,adminTitle:a.text(),editUrl:i.attr("href")});var f={getState:function(){return c},getValue:function(){return c&&c.id},setState:function(e){e?(u.val(e.id),a.text(e.adminTitle),r.removeClass("blank"),i.attr("href",e.editUrl)):(u.val(""),r.addClass("blank")),c=e},getTextLabel:function(e){if(!c)return null;var t=c.adminTitle;return e&&e.maxLength&&t.length>e.maxLength?t.substring(0,e.maxLength-1)+"…":t},focus:function(){o.default(".action-choose",r).focus()},openChooserModal:function(){var e=l;c&&c.parentId&&(e+=c.parentId+"/");var t={page_type:n.model_names.join(",")};n.can_choose_root&&(t.can_choose_root="true"),n.user_perms&&(t.user_perms=n.user_perms),ModalWorkflow({url:e,urlParams:t,onload:PAGE_CHOOSER_MODAL_ONLOAD_HANDLERS,responses:{pageChosen:function(e){f.setState(e)}}})},clear:function(){f.setState(null)}};return o.default(".action-choose",r).on("click",(function(){f.openChooserModal()})),o.default(".action-clear",r).on("click",(function(){f.clear()})),f}},73609:function(e){e.exports=jQuery}},t={};function n(r){if(t[r])return t[r].exports;var o=t[r]={id:r,loaded:!1,exports:{}};return e[r].call(o.exports,o,o.exports,n),o.loaded=!0,o.exports}n.m=e,n.x=function(){},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,{a:t}),t},n.d=function(e,t){for(var r in t)n.o(t,r)&&!n.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})},n.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),n.hmd=function(e){return(e=Object.create(e)).children||(e.children=[]),Object.defineProperty(e,"exports",{enumerable:!0,set:function(){throw new Error("ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: "+e.id)}}),e},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.j=957,function(){var e={957:0},t=[[45585,920],[90971,920]],r=function(){},o=function(o,a){for(var u,i,l=a[0],c=a[1],f=a[2],s=a[3],d=0,p=[];d<l.length;d++)i=l[d],n.o(e,i)&&e[i]&&p.push(e[i][0]),e[i]=0;for(u in c)n.o(c,u)&&(n.m[u]=c[u]);for(f&&f(n),o&&o(a);p.length;)p.shift()();return s&&t.push.apply(t,s),r()},a=self.webpackChunkwagtail=self.webpackChunkwagtail||[];function u(){for(var r,o=0;o<t.length;o++){for(var a=t[o],u=!0,i=1;i<a.length;i++){var l=a[i];0!==e[l]&&(u=!1)}u&&(t.splice(o--,1),r=n(n.s=a[0]))}return 0===t.length&&(n.x(),n.x=function(){}),r}a.forEach(o.bind(null,0)),a.push=o.bind(null,a.push.bind(a));var i=n.x;n.x=function(){return n.x=i||function(){},(r=u)()}}(),n.x()}();
//# sourceMappingURL=wagtail\admin\static\wagtailadmin\js\page-chooser.js.map