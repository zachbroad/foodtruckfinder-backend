!function(){"use strict";var e={923:function(e,n,t){var o=this&&this.__importDefault||function(e){return e&&e.__esModule?e:{default:e}};n.__esModule=!0;var r=o(t(73609));window.createTaskChooser=function(e){var n=r.default("#"+e+"-chooser"),t=n.find(".name"),o=r.default("#"+e),u=n.find(".action-edit");r.default(".action-choose",n).on("click",(function(){ModalWorkflow({url:n.data("chooserUrl"),onload:TASK_CHOOSER_MODAL_ONLOAD_HANDLERS,responses:{taskChosen:function(e){o.val(e.id),t.text(e.name),n.removeClass("blank"),u.attr("href",e.edit_url)}}})}))}},73609:function(e){e.exports=jQuery}},n={};function t(o){if(n[o])return n[o].exports;var r=n[o]={id:o,loaded:!1,exports:{}};return e[o].call(r.exports,r,r.exports,t),r.loaded=!0,r.exports}t.m=e,t.x=function(){},t.n=function(e){var n=e&&e.__esModule?function(){return e.default}:function(){return e};return t.d(n,{a:n}),n},t.d=function(e,n){for(var o in n)t.o(n,o)&&!t.o(e,o)&&Object.defineProperty(e,o,{enumerable:!0,get:n[o]})},t.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),t.hmd=function(e){return(e=Object.create(e)).children||(e.children=[]),Object.defineProperty(e,"exports",{enumerable:!0,set:function(){throw new Error("ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: "+e.id)}}),e},t.o=function(e,n){return Object.prototype.hasOwnProperty.call(e,n)},t.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},t.j=343,function(){var e={343:0},n=[[923,920],[90971,920]],o=function(){},r=function(r,u){for(var i,a,l=u[0],f=u[1],c=u[2],s=u[3],d=0,h=[];d<l.length;d++)a=l[d],t.o(e,a)&&e[a]&&h.push(e[a][0]),e[a]=0;for(i in f)t.o(f,i)&&(t.m[i]=f[i]);for(c&&c(t),r&&r(u);h.length;)h.shift()();return s&&n.push.apply(n,s),o()},u=self.webpackChunkwagtail=self.webpackChunkwagtail||[];function i(){for(var o,r=0;r<n.length;r++){for(var u=n[r],i=!0,a=1;a<u.length;a++){var l=u[a];0!==e[l]&&(i=!1)}i&&(n.splice(r--,1),o=t(t.s=u[0]))}return 0===n.length&&(t.x(),t.x=function(){}),o}u.forEach(r.bind(null,0)),u.push=r.bind(null,u.push.bind(u));var a=t.x;t.x=function(){return t.x=a||function(){},(o=i)()}}(),t.x()}();
//# sourceMappingURL=wagtail\admin\static\wagtailadmin\js\task-chooser.js.map