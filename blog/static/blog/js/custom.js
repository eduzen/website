!function(a){"function"==typeof define&&define.amd?define(a):"undefined"!=typeof module&&module.exports?module.exports=a():window.pym=a.call(this)}(function(){var a="xPYMx",b={},c=function(a){var b=document.createEvent("Event");b.initEvent("pym:"+a,!0,!0),document.dispatchEvent(b)},d=function(a){var b=new RegExp("[\\?&]"+a.replace(/[\[]/,"\\[").replace(/[\]]/,"\\]")+"=([^&#]*)"),c=b.exec(location.search);return null===c?"":decodeURIComponent(c[1].replace(/\+/g," "))},e=function(a,b){if(("*"===b.xdomain||a.origin.match(new RegExp(b.xdomain+"$")))&&"string"==typeof a.data)return!0},f=function(b,c,d){var e=["pym",b,c,d];return e.join(a)},g=function(b){var c=["pym",b,"(\\S+)","(.*)"];return new RegExp("^"+c.join(a)+"$")},h=Date.now||function(){return(new Date).getTime()},i=function(a,b,c){var d,e,f,g=null,i=0;c||(c={});var j=function(){i=c.leading===!1?0:h(),g=null,f=a.apply(d,e),g||(d=e=null)};return function(){var k=h();i||c.leading!==!1||(i=k);var l=b-(k-i);return d=this,e=arguments,l<=0||l>b?(g&&(clearTimeout(g),g=null),i=k,f=a.apply(d,e),g||(d=e=null)):g||c.trailing===!1||(g=setTimeout(j,l)),f}},j=function(){for(var a=b.autoInitInstances.length,c=a-1;c>=0;c--){var d=b.autoInitInstances[c];d.el.getElementsByTagName("iframe").length&&d.el.getElementsByTagName("iframe")[0].contentWindow||b.autoInitInstances.splice(c,1)}};return b.autoInitInstances=[],b.autoInit=function(a){var d=document.querySelectorAll("[data-pym-src]:not([data-pym-auto-initialized])"),e=d.length;j();for(var f=0;f<e;++f){var g=d[f];g.setAttribute("data-pym-auto-initialized",""),""===g.id&&(g.id="pym-"+f+"-"+Math.random().toString(36).substr(2,5));var h=g.getAttribute("data-pym-src"),i={xdomain:"string",title:"string",name:"string",id:"string",sandbox:"string",allowfullscreen:"boolean",parenturlparam:"string",parenturlvalue:"string",optionalparams:"boolean",trackscroll:"boolean",scrollwait:"number"},k={};for(var l in i)if(null!==g.getAttribute("data-pym-"+l))switch(i[l]){case"boolean":k[l]=!("false"===g.getAttribute("data-pym-"+l));break;case"string":k[l]=g.getAttribute("data-pym-"+l);break;case"number":var m=Number(g.getAttribute("data-pym-"+l));isNaN(m)||(k[l]=m);break;default:console.err("unrecognized attribute type")}var n=new b.Parent(g.id,h,k);b.autoInitInstances.push(n)}return a||c("pym-initialized"),b.autoInitInstances},b.Parent=function(a,b,c){this.id=a,this.url=b,this.el=document.getElementById(a),this.iframe=null,this.settings={xdomain:"*",optionalparams:!0,parenturlparam:"parentUrl",parenturlvalue:window.location.href,trackscroll:!1,scrollwait:100},this.messageRegex=g(this.id),this.messageHandlers={},c=c||{},this._constructIframe=function(){var a=this.el.offsetWidth.toString();this.iframe=document.createElement("iframe");var b="",c=this.url.indexOf("#");for(c>-1&&(b=this.url.substring(c,this.url.length),this.url=this.url.substring(0,c)),this.url.indexOf("?")<0?this.url+="?":this.url+="&",this.iframe.src=this.url+"initialWidth="+a+"&childId="+this.id,this.settings.optionalparams&&(this.iframe.src+="&parentTitle="+encodeURIComponent(document.title),this.iframe.src+="&"+this.settings.parenturlparam+"="+encodeURIComponent(this.settings.parenturlvalue)),this.iframe.src+=b,this.iframe.setAttribute("width","100%"),this.iframe.setAttribute("scrolling","no"),this.iframe.setAttribute("marginheight","0"),this.iframe.setAttribute("frameborder","0"),this.settings.title&&this.iframe.setAttribute("title",this.settings.title),void 0!==this.settings.allowfullscreen&&this.settings.allowfullscreen!==!1&&this.iframe.setAttribute("allowfullscreen",""),void 0!==this.settings.sandbox&&"string"==typeof this.settings.sandbox&&this.iframe.setAttribute("sandbox",this.settings.sandbox),this.settings.id&&(document.getElementById(this.settings.id)||this.iframe.setAttribute("id",this.settings.id)),this.settings.name&&this.iframe.setAttribute("name",this.settings.name);this.el.firstChild;)this.el.removeChild(this.el.firstChild);this.el.appendChild(this.iframe),window.addEventListener("resize",this._onResize),this.settings.trackscroll&&window.addEventListener("scroll",this._throttleOnScroll)},this._onResize=function(){this.sendWidth(),this.settings.trackscroll&&this.sendViewportAndIFramePosition()}.bind(this),this._onScroll=function(){this.sendViewportAndIFramePosition()}.bind(this),this._fire=function(a,b){if(a in this.messageHandlers)for(var c=0;c<this.messageHandlers[a].length;c++)this.messageHandlers[a][c].call(this,b)},this.remove=function(){window.removeEventListener("message",this._processMessage),window.removeEventListener("resize",this._onResize),this.el.removeChild(this.iframe),j()},this._processMessage=function(a){if(e(a,this.settings)&&"string"==typeof a.data){var b=a.data.match(this.messageRegex);if(!b||3!==b.length)return!1;var c=b[1],d=b[2];this._fire(c,d)}}.bind(this),this._onHeightMessage=function(a){var b=parseInt(a);this.iframe.setAttribute("height",b+"px")},this._onNavigateToMessage=function(a){document.location.href=a},this._onScrollToChildPosMessage=function(a){var b=document.getElementById(this.id).getBoundingClientRect().top+window.pageYOffset,c=b+parseInt(a);window.scrollTo(0,c)},this.onMessage=function(a,b){a in this.messageHandlers||(this.messageHandlers[a]=[]),this.messageHandlers[a].push(b)},this.sendMessage=function(a,b){this.el.getElementsByTagName("iframe").length&&(this.el.getElementsByTagName("iframe")[0].contentWindow?this.el.getElementsByTagName("iframe")[0].contentWindow.postMessage(f(this.id,a,b),"*"):this.remove())},this.sendWidth=function(){var a=this.el.offsetWidth.toString();this.sendMessage("width",a)},this.sendViewportAndIFramePosition=function(){var a=this.iframe.getBoundingClientRect(),b=window.innerWidth||document.documentElement.clientWidth,c=window.innerHeight||document.documentElement.clientHeight,d=b+" "+c;d+=" "+a.top+" "+a.left,d+=" "+a.bottom+" "+a.right,this.sendMessage("viewport-iframe-position",d)};for(var d in c)this.settings[d]=c[d];return this._throttleOnScroll=i(this._onScroll.bind(this),this.settings.scrollwait),this.onMessage("height",this._onHeightMessage),this.onMessage("navigateTo",this._onNavigateToMessage),this.onMessage("scrollToChildPos",this._onScrollToChildPosMessage),this.onMessage("parentPositionInfo",this.sendViewportAndIFramePosition),window.addEventListener("message",this._processMessage,!1),this._constructIframe(),this},b.Child=function(b){this.parentWidth=null,this.id=null,this.parentTitle=null,this.parentUrl=null,this.settings={renderCallback:null,xdomain:"*",polling:0,parenturlparam:"parentUrl"},this.timerId=null,this.messageRegex=null,this.messageHandlers={},b=b||{},this.onMessage=function(a,b){a in this.messageHandlers||(this.messageHandlers[a]=[]),this.messageHandlers[a].push(b)},this._fire=function(a,b){if(a in this.messageHandlers)for(var c=0;c<this.messageHandlers[a].length;c++)this.messageHandlers[a][c].call(this,b)},this._processMessage=function(a){if(e(a,this.settings)&&"string"==typeof a.data){var b=a.data.match(this.messageRegex);if(b&&3===b.length){var c=b[1],d=b[2];this._fire(c,d)}}}.bind(this),this._onWidthMessage=function(a){var b=parseInt(a);b!==this.parentWidth&&(this.parentWidth=b,this.settings.renderCallback&&this.settings.renderCallback(b),this.sendHeight())},this.sendMessage=function(a,b){window.parent.postMessage(f(this.id,a,b),"*")},this.sendHeight=function(){var a=document.getElementsByTagName("body")[0].offsetHeight.toString();return this.sendMessage("height",a),a}.bind(this),this.getParentPositionInfo=function(){this.sendMessage("parentPositionInfo")},this.scrollParentTo=function(a){this.sendMessage("navigateTo","#"+a)},this.navigateParentTo=function(a){this.sendMessage("navigateTo",a)},this.scrollParentToChildEl=function(a){var b=document.getElementById(a).getBoundingClientRect().top+window.pageYOffset;this.scrollParentToChildPos(b)},this.scrollParentToChildPos=function(a){this.sendMessage("scrollToChildPos",a.toString())};var g=function(a){var b,d=document.getElementsByTagName("html")[0],e=d.className;try{b=window.self!==window.top?"embedded":"not-embedded"}catch(a){b="embedded"}e.indexOf(b)<0&&(d.className=e?e+" "+b:b,a&&a(b),c("marked-embedded"))};this.remove=function(){window.removeEventListener("message",this._processMessage),this.timerId&&clearInterval(this.timerId)};for(var h in b)this.settings[h]=b[h];this.id=d("childId")||b.id,this.messageRegex=new RegExp("^pym"+a+this.id+a+"(\\S+)"+a+"(.*)$");var i=parseInt(d("initialWidth"));return this.parentUrl=d(this.settings.parenturlparam),this.parentTitle=d("parentTitle"),this.onMessage("width",this._onWidthMessage),window.addEventListener("message",this._processMessage,!1),this.settings.renderCallback&&this.settings.renderCallback(i),this.sendHeight(),this.settings.polling&&(this.timerId=window.setInterval(this.sendHeight,this.settings.polling)),g(b.onMarkedEmbeddedStatus),this},"undefined"!=typeof document&&b.autoInit(!0),b});
var pymChild = new pym.Child();

function calcular() {
    var topesEscalas = [33040, 66080, 99119, 132159, 198239, 264318, 396478, 528637, 99999999],
    porcentajesEscalas = [.05, .09, .12, .15, .19, .23, .27, .31, .35],
    // fijosEscalas = [1652, 4625, 8590, 13546, 26101, 41299, 76982, 117951],

    MINIMO_NO_IMPONIBLE = 103018.78, // CAMBIAMOS EL 14/8 UN 20% MAS
    ADICIONAL_4TA_CATEGORIA = 494490.16, // CAMBIAMOS EL 14/8 UN 20% MAS
    CONYUGE = 80033.97,
    HIJO = 40361.43,
    //agregar emplada domestica
    TOPE_APORTES = 16598.31
    TOPE_JUBILADO = 670255.20,
    TOPE_ALQUILER = 103018.78,
    TOPE_HIPOTECARIO = 20000;

    var sueldoBruto = $("#sueldoBruto").val(),
        isConyuge = $("input[name='conyuge']:checked").val(),
        isJubilado = $("input[name='jubilado']:checked").val(),
        isPatagonico = $("input[name='patagonico']:checked").val(),
        valorAlquiler = $("#alquiler").val(),
        deduccionAlquiler = 12 * valorAlquiler * .4 > TOPE_ALQUILER ? TOPE_ALQUILER : 12 * valorAlquiler * .4,
        valorHipotecario = $("#hipotecario").val(),
        deduccionHipotecario = 12 * valorHipotecario > TOPE_HIPOTECARIO ? TOPE_HIPOTECARIO : 12 * valorHipotecario,
        hijosElement = document.getElementById("hijos"),
        cantHijos = hijosElement.options[hijosElement.selectedIndex].value,
        sueldoNeto = 0 == isJubilado ? .17 * sueldoBruto > TOPE_APORTES ? sueldoBruto - TOPE_APORTES : .83 * sueldoBruto : .06 * sueldoBruto > TOPE_APORTES ? sueldoBruto - TOPE_APORTES : .94 * sueldoBruto;

    var sueldoNetoAnual = 13 * sueldoNeto,
        mniConDeduccionEspecial = (MINIMO_NO_IMPONIBLE + ADICIONAL_4TA_CATEGORIA) * (1.22 * isPatagonico + (1 - isPatagonico));
    mniTotal = (mniConDeduccionEspecial + CONYUGE * isConyuge + HIJO * cantHijos + deduccionAlquiler + deduccionHipotecario) * (1 - isJubilado) + isJubilado * (TOPE_JUBILADO + deduccionAlquiler + deduccionHipotecario),
        montoImponibleAplicable = 0,
        mniTotal < sueldoNetoAnual && (montoImponibleAplicable = sueldoNetoAnual - mniTotal);

    var result = calcularImpuesto(montoImponibleAplicable);
    impuestoAnual = result.value.toFixed(2), $("#impuestoAnual").text("$" + impuestoAnual);

    var impuestoMensual = (impuestoAnual / 13).toFixed(2);
    $("#impuestoMensual").text("$" + impuestoMensual);
    var alicuota = impuestoMensual / sueldoBruto * 100;
    $("#alicuota").text(alicuota.toFixed(2) + "%");
    var alicuotaMarginal = 0 == alicuota ? 0 : 100 * porcentajesEscalas[result.escala];
    $("#alicuotaMarginal").text(alicuotaMarginal.toFixed(2) + "%");
    var sueldoEnMano = sueldoNeto - impuestoMensual;
    $("#sueldoEnMano").html("$" + Math.round(sueldoEnMano) + ".00* <br> <span class='leyenda'>*En el cálculo se asume que el contribuyente descuenta el total de la deducción por hijos a cargo.</span>" )

    pymChild.scrollParentToChildEl('pn-result');
    pymChild.sendHeight();

}

function calcularImpuesto(monto) {
    var topesEscalas = [33040, 66080, 99119, 132159, 198239, 264318, 396478, 528637, 99999999];
    var porcentajesEscalas = [.05, .09, .12, .15, .19, .23, .27, .31, .35];
    var i = 0;
    var result = {};
    var value = 0;
    while(monto > topesEscalas[i]) {
        var diff = i == 0 ? topesEscalas[i] : topesEscalas[i] - topesEscalas[i - 1];
        value += diff * porcentajesEscalas[i];
        i++;
    }

    diff = i == 0 ? monto : monto - topesEscalas[i - 1];
    value += diff * porcentajesEscalas[i];

    result.value = value;
    result.escala = i;
    return result;
}

$(document).ready(function() {

    pymChild.sendHeight();

    var doit;
    window.onresize = function(d) {
        clearTimeout( doit );
        doit = setTimeout( function(){ pymChild.sendHeight(); }, 200 );
    };

    $("#calcular").on("click", function() {
        calcular()
    }), $(document).keypress(function(a) {
        13 == a.keyCode && (a.preventDefault(), calcular())
    }), $("input[name='jubilado']").click(function() {
        $("input[name='conyuge']").attr({
            disabled: 1 == $(this).val()
        }), $("input[name='patagonico']").attr({
            disabled: 1 == $(this).val()
        })
    })


     $('#alquiler').on('change', function(event) {
        event.preventDefault();
        if ($(this).val() !== '') {
            $("#hipotecario").val('');
            $("#hipotecario").attr("disabled", true);
        } else {
            $("#hipotecario").attr("disabled", false);
        }
    });
    $('#hipotecario').on('change', function(event) {
        event.preventDefault();
        if ($(this).val() !== '') {
            $("#alquiler").val('');
            $("#alquiler").attr("disabled", true);
        } else {
            $("#alquiler").attr("disabled", false);
        }
    });




});

/*var topesEscalas = [25800, 51600, 77400, 103200, 154800, 206400, 309600, 412800, 99999999],
    porcentajesEscalas = [.05, .09, .12, .15, .19, .23, .27, .31, .35],
    MINIMO_NO_IMPONIBLE = 66917.91,
    ADICIONAL_4TA_CATEGORIA = 321205.968,
    CONYUGE = 62385.2,
    HIJO = 31461.09,
    TOPE_APORTES = 13926.16,
    TOPE_JUBILADO = 407592,
    TOPE_ALQUILER = 51967,
    TOPE_HIPOTECARIO = 2e4;*/


