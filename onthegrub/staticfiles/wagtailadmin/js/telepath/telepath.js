!function(){"use strict";var t={14923:function(t){function n(t,o,i){return(n=r()?Reflect.construct:function(t,n,r){var o=[null];o.push.apply(o,n);var i=new(Function.bind.apply(t,o));return r&&e(i,r.prototype),i}).apply(null,arguments)}function r(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(t){return!1}}function e(t,n){return(e=Object.setPrototypeOf||function(t,n){return t.__proto__=n,t})(t,n)}function o(t,n){return function(t){if(Array.isArray(t))return t}(t)||function(t,n){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(t)){var r=[],e=!0,o=!1,i=void 0;try{for(var u,a=t[Symbol.iterator]();!(e=(u=a.next()).done)&&(r.push(u.value),!n||r.length!==n);e=!0);}catch(t){o=!0,i=t}finally{try{e||null==a.return||a.return()}finally{if(o)throw i}}return r}}(t,n)||i(t,n)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function i(t,n){if(t){if("string"==typeof t)return u(t,n);var r=Object.prototype.toString.call(t).slice(8,-1);return"Object"===r&&t.constructor&&(r=t.constructor.name),"Map"===r||"Set"===r?Array.from(t):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?u(t,n):void 0}}function u(t,n){(null==n||n>t.length)&&(n=t.length);for(var r=0,e=new Array(n);r<n;r++)e[r]=t[r];return e}function a(t){return(a="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t})(t)}function c(t,n){for(var r=0;r<n.length;r++){var e=n[r];e.enumerable=e.enumerable||!1,e.configurable=!0,"value"in e&&(e.writable=!0),Object.defineProperty(t,e.key,e)}}var f=function(){function t(){!function(t,n){if(!(t instanceof n))throw new TypeError("Cannot call a class as a function")}(this,t),this.constructors={}}var r,e;return r=t,(e=[{key:"register",value:function(t,n){this.constructors[t]=n}},{key:"unpack",value:function(t){var n={};return this.scanForIds(t,n),this.unpackWithRefs(t,n,{})}},{key:"scanForIds",value:function(t,n){var r=this;if(null!==t&&"object"===a(t))if(Array.isArray(t))t.forEach((function(t){return r.scanForIds(t,n)}));else{var e=!1;if("_id"in t&&(e=!0,n[t._id]=t),("_type"in t||"_val"in t||"_ref"in t)&&(e=!0),"_list"in t&&(e=!0,t._list.forEach((function(t){return r.scanForIds(t,n)}))),"_args"in t&&(e=!0,t._args.forEach((function(t){return r.scanForIds(t,n)}))),"_dict"in t){e=!0;for(var i=0,u=Object.entries(t._dict);i<u.length;i++){var c=o(u[i],2),f=(c[0],c[1]);this.scanForIds(f,n)}}if(!e)for(var l=0,s=Object.entries(t);l<s.length;l++){var p=o(s[l],2),y=(p[0],p[1]);this.scanForIds(y,n)}}}},{key:"unpackWithRefs",value:function(t,r,e){var c,f,l=this;if(null===t||"object"!==a(t))return t;if(Array.isArray(t))return t.map((function(t){return l.unpackWithRefs(t,r,e)}));if("_ref"in t)c=t._ref in e?e[t._ref]:this.unpackWithRefs(r[t._ref],r,e);else if("_val"in t)c=t._val;else if("_list"in t)c=t._list.map((function(t){return l.unpackWithRefs(t,r,e)}));else if("_dict"in t){c={};for(var s=0,p=Object.entries(t._dict);s<p.length;s++){var y=o(p[s],2),h=y[0],d=y[1];c[h]=this.unpackWithRefs(d,r,e)}}else{if(!("_type"in t)){if("_id"in t)throw new Error("telepath encountered object with _id but no type specified");c={};for(var b=0,v=Object.entries(t);b<v.length;b++){var m=o(v[b],2),_=m[0],g=m[1];c[_]=this.unpackWithRefs(g,r,e)}return c}var w=t._type;c=n(this.constructors[w],function(t){if(Array.isArray(t))return u(t)}(f=t._args.map((function(t){return l.unpackWithRefs(t,r,e)})))||function(t){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(t))return Array.from(t)}(f)||i(f)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}())}return"_id"in t&&(e[t._id]=c),c}}])&&c(r.prototype,e),t}();t.exports=f},81249:function(t,n,r){var e=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};n.__esModule=!0;var o=e(r(14923));window.telepath=new o.default}},n={};function r(e){if(n[e])return n[e].exports;var o=n[e]={id:e,loaded:!1,exports:{}};return t[e].call(o.exports,o,o.exports,r),o.loaded=!0,o.exports}r.m=t,r.x=function(){},r.n=function(t){var n=t&&t.__esModule?function(){return t.default}:function(){return t};return r.d(n,{a:n}),n},r.d=function(t,n){for(var e in n)r.o(n,e)&&!r.o(t,e)&&Object.defineProperty(t,e,{enumerable:!0,get:n[e]})},r.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(t){if("object"==typeof window)return window}}(),r.hmd=function(t){return(t=Object.create(t)).children||(t.children=[]),Object.defineProperty(t,"exports",{enumerable:!0,set:function(){throw new Error("ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: "+t.id)}}),t},r.o=function(t,n){return Object.prototype.hasOwnProperty.call(t,n)},r.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},r.j=987,function(){var t={987:0},n=[[81249,920],[90971,920]],e=function(){},o=function(o,i){for(var u,a,c=i[0],f=i[1],l=i[2],s=i[3],p=0,y=[];p<c.length;p++)a=c[p],r.o(t,a)&&t[a]&&y.push(t[a][0]),t[a]=0;for(u in f)r.o(f,u)&&(r.m[u]=f[u]);for(l&&l(r),o&&o(i);y.length;)y.shift()();return s&&n.push.apply(n,s),e()},i=self.webpackChunkwagtail=self.webpackChunkwagtail||[];function u(){for(var e,o=0;o<n.length;o++){for(var i=n[o],u=!0,a=1;a<i.length;a++){var c=i[a];0!==t[c]&&(u=!1)}u&&(n.splice(o--,1),e=r(r.s=i[0]))}return 0===n.length&&(r.x(),r.x=function(){}),e}i.forEach(o.bind(null,0)),i.push=o.bind(null,i.push.bind(i));var a=r.x;r.x=function(){return r.x=a||function(){},(e=u)()}}(),r.x()}();
//# sourceMappingURL=wagtail\admin\static\wagtailadmin\js\telepath\telepath.js.map