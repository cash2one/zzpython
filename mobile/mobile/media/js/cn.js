/*! beacon.js ver.44 */
(function() {
    var a = true;
    if (window.MAGNETO === undefined) {
        MAGNETO = {};
        a = false
    }
    MAGNETO.globals = {
        win: window,
        doc: document,
        opener: opener,
        pageId: null,
        jsUrlRoot: "http://style.china.alibaba.com/sys/js/beacon/v1/",
        customize: window.WolfSmoke || {},
        protocol: document.location.protocol,
        isConflicted: a,
        version: "44"
    }
})(); (function(a) {
    var b = a.globals,
    c = b.customize;
    a.config = {
        samplerate: c.samplerate || 1,
        siteNo: c.siteNo || 2,
        logSeverOne: b.protocol + "//dmtracking.alibaba.com/b.jpg",
        logSeverTwo: b.protocol + "//dmtracking.alibaba.com/c.jpg",
        tracelogSever: b.protocol + "//stat.china.alibaba.com/tracelog/click.html",
        errorSever: b.protocol + "//stat.china.alibaba.com/dw/error.html",
        acookieSever: b.protocol + "//acookie.alibaba.com/1.gif",
        isSetCookieToAcookie: c.isSetCookieToAcookie || true,
        needDefaultCookies: ["cna", "ali_apache_id"],
        isCheckLogin: true
    }
})(MAGNETO); (function(h) {
    var k = h.globals,
    b = h.config,
    j = k.doc,
    e = !!j.attachEvent,
    f = "attachEvent",
    d = "addEventListener",
    g = "detachEvent",
    c = "removeEventListener",
    a = e ? f: d,
    i = e ? g: c;
    h.tools = {
        is: function(l, m) {
            return l != null && Object(l) instanceof m
        },
        isFunction: function(l) {
            return (typeof l === "function") || Object.prototype.toString.apply(l) === "[object Function]"
        },
        isNumber: function(l) {
            return typeof l === "number" && isFinite(l)
        },
        isString: function(l) {
            return typeof l === "string"
        },
        isArray: Array.isArray ||
        function(l) {
            return Object.prototype.toString.apply(l) === "[object Array]"
        },
        isEmptyObject: function(m) {
            for (var l in m) {
                return false
            }
            return true
        },
        spmMeta: function() {
            var p = document.getElementsByTagName("meta"),
            n = 0,
            o,
            m = p.length,
            l;
            for (o = 0; o < m; o++) {
                l = p[o];
                if (this.tryToGetAttribute(l, "name") === "data-spm") {
                    n = this.tryToGetAttribute(l, "content");
                    break
                }
            }
            return n
        },
        trim: function(l) {
            return this.isString(l) ? l.replace(/^\s+|\s+$/g, "") : ""
        },
        tryToGetHref: function(m) {
            var n = this;
            var l;
            try {
                l = this.trim(m.getAttribute("href", 2))
            } catch(o) {}
            return l || ""
        },
        tryToGetAttribute: function(l, m) {
            return l && l.getAttribute ? (l.getAttribute(m) || "") : ""
        },
        tryToSetAttribute: function(l, o, m) {
            if (l && l.setAttribute) {
                try {
                    l.setAttribute(o, m)
                } catch(n) {}
            }
        },
        tryToRemoveAttribute: function(l, n) {
            if (l && l.removeAttribute) {
                try {
                    l.removeAttribute(n)
                } catch(m) {
                    tryToSetAttribute(l, n, "")
                }
            }
        },
        nodeListToArray: function(m) {
            var l, p;
            try {
                l = [].slice.call(m);
                return l
            } catch(o) {
                l = [];
                p = m.length;
                for (var n = 0; n < p; n++) {
                    l.push(m[n])
                }
                return l
            }
        },
        combineJson: function(p, o, q) {
            var m = {};
            for (var n in o) {
                if (q || !p.hasOwnProperty(n)) {
                    m[n] = o[n];
                    delete p[n]
                }
            }
            for (var l in p) {
                m[l] = p[l]
            }
            return m
        },
        combineParam: function(r, m, o, s) {
            var l = [];
            for (var q in m) {
                if (s || !r.hasOwnProperty(q)) {
                    l.push(q + "=" + m[q]);
                    delete r[q]
                }
            }
            for (var n in r) {
                l.push(n + "=" + r[n])
            }
            return l.join(o)
        },
        parseParam: function(o, r) {
            var q, m = null,
            p = {};
            if (this.isString(o) && o.length > 0) {
                q = o.split(r);
                for (var n = 0,
                l = q.length; n < l; ++n) {
                    m = q[n].split("=");
                    p[m[0]] = m[1]
                }
            }
            return p
        },
        on: function(n, l, m) {
            n[a]((e ? "on": "") + l,
            function(p) {
                p = p || win.event;
                var o = p.target || p.srcElement;
                m(p, o)
            },
            false)
        },
        off: function(n, l, m) {
            n[i]((e ? "on": "") + l,
            function(p) {
                p = p || win.event;
                var o = p.target || p.srcElement;
                m(p, o)
            },
            false)
        },
        random: function() {
            return Math.round(Math.random() * 2147483647)
        },
        getReferrer: function() {
            var l, m = k.doc.referrer;
            try {
                l = m || k.opener.location.href || "-"
            } catch(n) {
                l = "-"
            }
            return l
        },
        sampling: function() {
            return (Math.random() - b.samplerate) <= 0
        },
        trimHttpStr: function(l) {
            return l.substr(l.indexOf("://") + 2)
        },
        randomPageId: function() {
            var l = k.win.dmtrack_pageid || "",
            n = +new Date(),
            m = "";
            l += n;
            l = l.substr(0, 20);
            while (l.length < 42) {
                l += this.random()
            }
            m = l.substr(0, 42);
            k.pageId = m;
            k.win.dmtrack_pageid = m;
            return m
        },
        sendErrorInfo: function(o, n) {
            var l = b.errorSever,
            m = h.moduleManager.require("recorder"),
            p = {
                type: n,
                exception: o.message
            };
            m.send(l, p)
        },
        emptyFunction: function() {}
    }
})(MAGNETO); (function(a) {
    a.moduleManager = function() {
        var f = a.globals,
        e = f.doc,
        d = a.tools,
        c = {},
        b = function(i) {
            var h = f.jsUrlHash[i];
            return h ? f.jsUrlRoot + h: null
        },
        g = function() {
            var h = function(j, k) {
                var l, i = e.createElement("script");
                i.src = j;
                if (k) {
                    i.onload = i.onreadystatechange = function() {
                        if (!this.readyState || "loaded" === i.readyState || "complete" === i.readyState) {
                            i.onload = i.onreadystatechange = null;
                            k()
                        }
                    }
                }
                l = e.getElementsByTagName("script")[0];
                l.parentNode.insertBefore(i, l)
            };
            return {
                load: h
            }
        } ();
        return {
            register: function(k, h, j) {
                var i = this;
                if (i.hasRegistered(k)) {
                    return
                }
                c[k] = j ? h.call(a) : h
            },
            require: function(h, p) {
                var j = c[h],
                r;
                if (d.isFunction(j)) {
                    return c[h] = j.call(a)
                } else {
                    if (j) {
                        return j
                    }
                }
                r = b(h);
                var k = false,
                q = document.head || document.getElementsByTagName("head")[0],
                n = q.getElementsByTagName("script");
                for (var o = 0,
                m = n.length; o < m; o++) {
                    if (n[o].src === r) {
                        k = true
                    }
                }
                if (!k && r !== null) {
                    g.load(r,
                    function() {
                        c[h] = c[h].call(a); (p || d.emptyFunction).call(null, c[h])
                    })
                }
                return null
            },
            hasRegistered: function(h) {
                return !! c[h]
            },
            hadUsed: function(i) {
                var h = c[i];
                return h && !d.isFunction(h)
            }
        }
    } ()
})(MAGNETO); (function(a) {
    a.moduleManager.register("recorder",
    function() {
        var g = this,
        e = g.globals,
        c = g.tools,
        f = function(k, l, m) {
            var j = new Image(1, 1);
            j.src = k + "?" + l;
            j.onload = function() {
                this.onload = null; (m || c.emptyFunction)()
            }
        },
        i = function(j, m, n) {
            var k = e.win.XDomainRequest,
            l;
            if (k) {
                l = new k;
                l.open("POST", j)
            } else {
                l = new XMLHttpRequest;
                if ("withCredentials" in l) {
                    l.open("POST", j, true);
                    l.setRequestHeader("Content-Type", "text/plain")
                }
            }
            if (l) {
                l.onreadystatechange = function() {
                    if (l.readyState == 4) {
                        n && n();
                        l = null
                    }
                };
                l.send(m);
                return true
            }
            return false
        },
        b = function() {},
        d = function(q) {
            var k = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
            p, o, m, j = q.length,
            n = 0,
            l = "";
            while (n < j) {
                p = q.charCodeAt(n++) & 255;
                if (n == j) {
                    l += k.charAt(p >> 2);
                    l += k.charAt((p & 3) << 4);
                    l += "==";
                    break
                }
                o = q.charCodeAt(n++);
                if (n == j) {
                    l += k.charAt(p >> 2);
                    l += k.charAt(((p & 3) << 4) | ((o & 240) >> 4));
                    l += k.charAt((o & 15) << 2);
                    l += "=";
                    break
                }
                m = q.charCodeAt(n++);
                l += k.charAt(p >> 2);
                l += k.charAt(((p & 3) << 4) | ((o & 240) >> 4));
                l += k.charAt(((o & 15) << 2) | ((m & 192) >> 6));
                l += k.charAt(m & 63)
            }
            return l
        },
        h = function(m, j) {
            var n = "",
            k = "",
            l = [];
            if (m && !c.isEmptyObject(m)) {
                n = d(c.combineParam(m, {},
                "&"))
            }
            j.ver = e.version;
            j.t = +new Date();
            k = c.combineParam(j, {},
            "&");
            if (n) {
                l.push(n)
            }
            if (k) {
                l.push(k)
            }
            return l.join("&")
        };
        return {
            sendEssentialInfo: function(k, l, j, o) {
                var m = this,
                n = h(l, j);
                m.send(k, n, o)
            },
            send: function(k, m, n) {
                var j = m.length;
                if (j <= 2036) {
                    f(k, m, n)
                } else {
                    if (j <= 8192) {
                        f(k, "len=" + j + "&" + m, n)
                    } else {
                        f(k, "err=len&len=" + j + "&" + m, n)
                    }
                }
            }
        }
    },
    true)
})(MAGNETO); (function(a) {
    a.moduleManager.register("cookieProcessor",
    function() {
        var f = this,
        c = f.tools,
        e = f.globals,
        d = e.doc,
        h = function(n) {
            var q = n.split(/;\s/g),
            l = null,
            o = null,
            k = null,
            p = {};
            if (c.isString(n) && n.length > 0) {
                for (var m = 0,
                j = q.length; m < j; m++) {
                    k = q[m].match(/([^=]+)=/i);
                    if (k instanceof Array) {
                        l = unescape(k[1]);
                        o = unescape(q[m].substring(k[1].length + 1))
                    } else {
                        l = unescape(q[m]);
                        o = ""
                    }
                    p[l] = o
                }
            }
            return p
        },
        b = function(j) {
            var i = new Date;
            j = new Date(i.getTime() + j);
            return ";expires=" + j.toGMTString()
        },
        g = function(j, l, i, n, k, m) {
            var o = escape(j) + "=" + escape(l);
            if (i instanceof Date) {
                o += "; expires=" + i.toUTCString()
            }
            if (c.isNumber(i) && i !== 0) {
                o += b(i * 24 * 60 * 60 * 1000)
            }
            if (c.isString(n) && n !== "") {
                o += "; path=" + n
            }
            if (c.isString(k) && k !== "") {
                o += "; domain=" + k
            }
            if (m === true) {
                o += "; secure"
            }
            return o
        };
        return {
            get: function(i) {
                if (!c.isString(i) || i === "") {
                    return null
                }
                var j = h(d.cookie);
                return i in j ? j[i] : null
            },
            getSub: function(i, j) {
                var k = this.getSubCookies(i);
                if (k) {
                    if (!c.isString(j) || j === "") {
                        return null
                    }
                    return j in k ? k[j] : null
                } else {
                    return null
                }
            },
            getSubCookies: function(i) {
                var j = this.get(i),
                k;
                if (j) {
                    k = c.parseParam(j, "|");
                    return k
                } else {
                    return null
                }
            },
            set: function(j, k, i) {
                i = i || {};
                if (c.isString(j) && k !== undefined) {
                    var l = g(j, k, i.expires, i.path, i.domain, i.secure);
                    d.cookie = l
                }
            },
            setSub: function(j, l, k, i) {
                if (!c.isString(j) || j === "") {
                    return
                }
                if (!c.isString(l) || l === "") {
                    return
                }
                if (!k) {
                    return
                }
                var m = this.getSubCookies(j),
                n = {};
                if (m === null) {
                    m = {}
                }
                n[l] = k;
                this.set(j, c.combineParam(m, n, "|", true), i)
            },
            setSubs: function(j, l, i) {
                if (!c.isString(j) || j === "") {
                    return
                }
                var k = this.getSubCookies(j) || {};
                this.set(j, c.combineParam(k, l, "|", true), i)
            },
            remove: function(j, i) {
                i = i || {};
                var k = g(j, "", new Date(0), i.path, i.domain, i.secure);
                d.cookie = k
            },
            removeSub: function(i, j) {
                if (!c.isString(i) || i === "") {
                    return
                }
                if (!c.isString(j) || j === "") {
                    return
                }
                var k = this.getSubCookies(i);
                if (k && k.hasOwnProperty(j)) {
                    delete k[j];
                    this.set(i, c.combineParam(k, {},
                    "|"))
                }
            }
        }
    },
    true)
})(MAGNETO); (function(a) {
    a.moduleManager.register("ua",
    function() {
        var k = this,
        q = k.globals,
        o = {
            trident: 0,
            webkit: 0,
            gecko: 0,
            presto: 0,
            khtml: 0,
            name: "other",
            ver: null
        },
        i = {
            ie: 0,
            firefox: 0,
            chrome: 0,
            safari: 0,
            opera: 0,
            konq: 0,
            name: "other",
            ver: null
        },
        j = {
            name: "",
            ver: null
        },
        c = {
            win: false,
            mac: false,
            x11: false,
            name: "other"
        },
        d = "other",
        e = q.win,
        p = e.navigator,
        b = p.userAgent,
        f = p.platform,
        h,
        l,
        g = function(r) {
            var t = 0;
            return parseFloat(r.replace(/\./g,
            function() {
                return (t++===0) ? ".": ""
            }))
        };
        if (e.opera) {
            o.ver = i.ver = g(e.opera.version());
            o.presto = i.opera = parseFloat(o.ver);
            o.name = "presto";
            i.name = "opera"
        } else {
            if (/AppleWebKit\/(\S+)/.test(b)) {
                o.ver = g(RegExp["$1"]);
                o.webkit = o.ver;
                o.name = "webkit";
                if (/Chrome\/(\S+)/.test(b)) {
                    i.ver = g(RegExp["$1"]);
                    i.chrome = i.ver;
                    i.name = "chrome"
                } else {
                    if (/Version\/(\S+)/.test(b)) {
                        i.ver = g(RegExp["$1"]);
                        i.safari = i.ver;
                        i.name = "safari"
                    } else {
                        var n = 1;
                        if (o.webkit < 100) {
                            n = 1
                        } else {
                            if (o.webkit < 312) {
                                n = 1.2
                            } else {
                                if (o.webkit < 412) {
                                    n = 1.3
                                } else {
                                    n = 2
                                }
                            }
                        }
                        i.safari = i.ver = n;
                        i.name = "safari"
                    }
                }
            } else {
                if (/KHTML\/(\S+)/.test(b) || /Konqueror\/([^;]+)/.test(b)) {
                    o.ver = i.ver = g(RegExp["$1"]);
                    o.khtml = i.konq = o.ver;
                    o.name = "khtml";
                    i.name = "konq"
                } else {
                    if (/rv:([^\)]+)\) Gecko\/\d{8}/.test(b)) {
                        o.ver = g(RegExp["$1"]);
                        o.gecko = o.ver;
                        o.name = "gecko";
                        if (/Firefox\/(\S+)/.test(b)) {
                            i.ver = g(RegExp["$1"]);
                            i.firefox = i.ver;
                            i.name = "firefox"
                        }
                    } else {
                        if (/MSIE ([^;]+)/.test(b)) {
                            o.ver = i.ver = g(RegExp["$1"]);
                            o.trident = i.ie = o.ver;
                            o.name = "trident";
                            i.name = "ie"
                        }
                    }
                }
            }
        }
        j.name = i.name;
        j.ver = i.ver;
        if (h = b.match(/360SE/)) {
            j.name = "se360";
            j.ver = 3
        } else {
            if ((h = b.match(/Maxthon/)) && (l = e.external)) {
                j.name = "maxthon";
                try {
                    j.ver = g(l.max_version)
                } catch(m) {
                    j.ver = 0.1
                }
            } else {
                if (h = b.match(/TencentTraveler\s([\d.]*)/)) {
                    j.name = "tt";
                    j.ver = g(h[1]) || 0.1
                } else {
                    if (h = b.match(/TheWorld/)) {
                        j.name = "theworld";
                        j.ver = 3
                    } else {
                        if (h = b.match(/SE\s([\d.]*)/)) {
                            j.name = "sougou";
                            j.ver = g(h[1]) || 0.1
                        }
                    }
                }
            }
        }
        c.win = f.indexOf("Win") == 0;
        c.mac = f.indexOf("Mac") == 0;
        c.x11 = (f == "X11") || (f.indexOf("Linux") == 0);
        if (c.win) {
            if (/Win(?:dows )?([^do]{2})\s?(\d+\.\d+)?/.test(b)) {
                if (RegExp["$1"] == "NT") {
                    switch (RegExp["$2"]) {
                    case "5.1":
                        c.win = "XP";
                        break;
                    case "6.1":
                        c.win = "7";
                        break;
                    case "5.0":
                        c.win = "2000";
                        break;
                    case "6.0":
                        c.win = "Vista";
                        break;
                    default:
                        c.win = "NT";
                        break
                    }
                } else {
                    if (RegExp["$1"] == "9x") {
                        c.win = "ME"
                    } else {
                        c.win = RegExp["$1"]
                    }
                }
            }
            c.name = "windows" + c.win
        }
        if (c.mac) {
            c.name = "mac"
        }
        if (c.x11) {
            c.name = "x11"
        }
        if (c.win == "CE") {
            d = "windows mobile"
        } else {
            if (/ Mobile\//.test(b)) {
                d = "apple"
            } else {
                if ((h = b.match(/NokiaN[^\/]*|Android \d\.\d|webOS\/\d\.\d/))) {
                    d = h[0].toLowerCase()
                }
            }
        }
        return {
            engine: o,
            browser: i,
            extraBrowser: j,
            system: c,
            mobile: d,
            resolution: e.screen.width + "*" + e.screen.height,
            language: p.language || p.browserLanguage
        }
    })
})(MAGNETO); (function(a) {
    a.moduleManager.register("spm",
    function() {
        var v = true,
        k = false,
        j = "data-spm",
        K = "data-spm-anchor-id",
        R = "data-spm-protocol",
        b = "::-plain-::",
        p = a.globals,
        h = this.tools,
        P = window,
        l = P.document,
        H = k,
        E = {},
        q = k,
        s = "",
        M = "",
        L = "http://stat.china.alibaba.com/spm.html",
        o = k,
        d = function(T, G) {
            return T.indexOf(G) > -1
        },
        g = function(T, G) {
            return T.indexOf(G) == 0
        },
        F = function() {
            return Math.floor(Math.random() * 268435456).toString(16)
        },
        n = function(X) {
            var G = [],
            W,
            T;
            for (W in X) {
                if (X.hasOwnProperty(W)) {
                    T = "" + X[W];
                    G.push(g(W, b) ? T: (W + "=" + encodeURIComponent(T)))
                }
            }
            return G.join("&")
        },
        B = function(T) {
            var W = [],
            Y,
            X,
            Z,
            G = T.length;
            for (Z = 0; Z < G; Z++) {
                Y = T[Z][0];
                X = T[Z][1];
                W.push(g(Y, s_plain_obj) ? X: (Y + "=" + encodeURIComponent(X)))
            }
            return W.join("&")
        },
        A = function(W, Y) {
            var T = new Image(),
            aa = "_img_" + Math.random(),
            X = W.indexOf("?") == -1 ? "?": "&",
            Z,
            G = Y ? (h.isArray(Y) ? B(Y) : n(Y)) : "";
            P[aa] = T;
            T.onload = T.onerror = function() {
                P[aa] = null
            };
            T.src = Z = G ? (W + X + G) : W;
            T = null;
            return Z
        },
        x = function() {
            return l.getElementsByTagName("meta")
        },
        t = function() {
            var Y = x(),
            W,
            T,
            X,
            G;
            for (W = 0, T = Y.length; W < T; W++) {
                X = Y[W];
                G = h.tryToGetAttribute(X, "name");
                if (G == j) {
                    s = h.tryToGetAttribute(X, R);
                    M = h.tryToGetAttribute(X, "content")
                }
            }
        },
        w = function() {
            var W, T, G;
            t();
            if (P._SPM_a && P._SPM_b) {
                W = P._SPM_a.replace(/^{(\w+)}$/g, "$1");
                T = P._SPM_b.replace(/^{(\w+)}$/g, "$1");
                H = v
            } else {
                W = M;
                T = h.tryToGetAttribute(l.body, j) || 0
            }
            G = W + "." + T;
            if (!W || !T || !/^[\w\-\*]+\.[\w\-\*]+$/.test(G)) {
                G = 0
            }
            return G
        },
        J = function(T) {
            var G;
            while ((T = T.parentNode) && T.tagName != "BODY") {
                G = h.tryToGetAttribute(T, R);
                if (G) {
                    return G
                }
            }
            return ""
        },
        e = function(G) {
            if (P.jQuery) {
                jQuery(l).ready(G)
            } else {
                if (l.readyState === "complete") {
                    G()
                } else {
                    h.on(P, "load", G)
                }
            }
        },
        Q = function() {
            if (q) {
                return
            }
            if (!P.spmData) {
                if (!o) {
                    setTimeout(arguments.callee, 100)
                }
                return
            }
            q = v;
            var X = P.spmData["data"],
            W,
            G,
            Y,
            T;
            if (!X || !h.isArray(X)) {
                return
            }
            for (W = 0, G = X.length; W < G; W++) {
                Y = X[W];
                T = Y.xpath;
                E[T] = {
                    spmc: Y.spmc,
                    spmd: Y.spmd
                }
            }
        },
        O = function(Y) {
            var aa = l.getElementsByTagName("*"),
            T,
            X,
            W,
            ab,
            Z,
            G;
            for (T = []; Y && Y.nodeType == 1; Y = Y.parentNode) {
                if (Y.id) {
                    G = Y.id;
                    ab = 0;
                    for (X = 0; X < aa.length; X++) {
                        Z = aa[X];
                        if (Z.id && Z.id == G) {
                            ab++;
                            break
                        }
                    }
                    if (ab == 1) {
                        T.unshift('id("' + G + '")');
                        return T.join("/")
                    } else {
                        T.unshift(Y.tagName.toLowerCase() + '[@id="' + G + '"]')
                    }
                } else {
                    for (X = 1, W = Y.previousSibling; W; W = W.previousSibling) {
                        if (W.tagName == Y.tagName) {
                            X++
                        }
                    }
                    T.unshift(Y.tagName.toLowerCase() + "[" + X + "]")
                }
            }
            return T.length ? "/" + T.join("/") : null
        },
        f = function(G) {
            var T = E[O(G)];
            return T ? T.spmc: ""
        },
        U = function(G) {
            return G ? ( !! G.match(/^[^\?]*\balipay\.(?:com|net)\b/i)) : false
        },
        D = function(T) {
            var X, G, W;
            if (H) {
                G = O(T);
                W = E[G];
                if (W) {
                    X = W.spmd
                }
            } else {
                X = h.tryToGetAttribute(T, j);
                if (!X || !X.match(/^d\w+$/)) {
                    X = ""
                }
            }
            return X
        },
        i = function(W) {
            var X = l.getElementsByTagName("a"),
            G = X.length,
            T;
            for (T = 0; T < G; T++) {
                if (X[T] === W) {
                    return T + 1
                }
            }
            return 0
        },
        V = function(W, ac) {
            if (W && /&?\bspm=[^&#]*/.test(W)) {
                W = W.replace(/&?\bspm=[^&#]*/g, "").replace(/&{2,}/g, "&").replace(/\?&/, "?").replace(/\?$/, "")
            }
            if (!ac) {
                return W
            }
            var ad, Z, ab, aa = "&",
            X, T, G, Y;
            if (W.indexOf("#") != -1) {
                ab = W.split("#");
                W = ab.shift();
                Z = ab.join("#")
            }
            X = W.split("?");
            T = X.length - 1;
            ab = X[0].split("//");
            ab = ab[ab.length - 1].split("/");
            G = ab.length > 1 ? ab.pop() : "";
            if (T > 0) {
                ad = X.pop();
                W = X.join("?")
            }
            if (ad && T > 1 && ad.indexOf("&") == -1 && ad.indexOf("%") != -1) {
                aa = "%26"
            }
            W = W + "?spm=" + ac + (ad ? (aa + ad) : "") + (Z ? ("#" + Z) : "");
            Y = d(G, ".") ? G.split(".").pop().toLowerCase() : "";
            if (Y) {
                if (({
                    png: 1,
                    jpg: 1,
                    jpeg: 1,
                    gif: 1,
                    bmp: 1,
                    swf: 1
                }).hasOwnProperty(Y)) {
                    return 0
                }
                if (!ad && T <= 1) {
                    if (!Z && !({
                        htm: 1,
                        html: 1,
                        php: 1
                    }).hasOwnProperty(Y)) {
                        W += "&file=" + G
                    }
                }
            }
            return W
        },
        C = function(Y, G) {
            var X = Y,
            W = h.tryToGetHref(X),
            Z = (h.tryToGetAttribute(X, R) || J(X) || s) == "i",
            T = L + "?spm=";
            if (!W || !G) {
                return
            }
            if (W.indexOf("#") === 0 || W.toLowerCase().indexOf("javascript:") === 0 || U(W)) {
                return
            }
            if (Z) {
                T += G + "&url=" + encodeURIComponent(W) + "&cache=" + F();
                A(T)
            } else { (W = V(W, G)) && r(X, W)
            }
        },
        r = function(Y, W) {
            var X = Y,
            G, T = X.innerHTML;
            if (T && T.indexOf("<") == -1) {
                G = l.createElement("b");
                G.style.display = "none";
                X.appendChild(G)
            }
            X.href = W;
            if (G) {
                X.removeChild(G)
            }
        },
        I = function(T) {
            var G;
            return (T && (G = T.match(/&?\bspm=([^&#]*)/))) ? G[1] : ""
        },
        u = function(X) {
            var W = X,
            T = D(W) || i(W),
            G = [w(), 0, T].join(".");
            C(W, G)
        },
        z = function(W) {
            var G, T = W.tagName.toLowerCase(),
            X = {};
            while (W && T !== "html" && T !== "body") {
                if (!H) {
                    G = h.tryToGetAttribute(W, j)
                } else {
                    G = f(W)
                }
                if (G) {
                    X = {
                        spmEl: W,
                        spmId: G
                    };
                    break
                }
                if (! (W = W.parentNode)) {
                    break
                }
            }
            return X
        },
        m = function(X, ae) {
            var W = X,
            ac = ae.spmEl,
            ag = ae.spmId,
            af = [w(), ag].join(".");
            if (!af.match || !af.match(/^[\w\-\*]+\.[\w\-\*]+\.[\w\-\*]+$/)) {
                return
            }
            var Y = parseInt(h.tryToGetAttribute(ac, "data-spm-max-idx"), 10) || 0,
            aj = h.nodeListToArray(ac.getElementsByTagName("a")),
            ai = h.nodeListToArray(ac.getElementsByTagName("area")),
            T = aj.concat(ai),
            ah = T.length,
            ab,
            aa,
            G,
            ad,
            Z;
            if (ah < 50) {
                for (ab = 0, anchorIdx = Y; ab < ah; ab++) {
                    aa = T[ab];
                    G = h.tryToGetHref(aa);
                    Z = z(aa.parentNode);
                    if (!G) {
                        continue
                    }
                    if (Z.spmEl !== ac) {
                        continue
                    }
                    if (h.tryToGetAttribute(aa, K)) {
                        continue
                    }
                    anchorIdx++;
                    ad = af + "." + (D(aa) || anchorIdx);
                    h.tryToSetAttribute(aa, K, ad)
                }
                h.tryToSetAttribute(ac, "data-spm-max-idx", anchorIdx)
            } else {
                for (ab = 0; ab < ah; ab++) {
                    aa = T[ab];
                    G = h.tryToGetHref(aa);
                    if (!G) {
                        continue
                    }
                    if (aa === W) {
                        ad = af + "." + (D(aa) || ab);
                        h.tryToSetAttribute(aa, K, ad);
                        break
                    }
                }
            }
        },
        y = function(T) {
            var G = T,
            W = h.tryToGetAttribute(G, K),
            X;
            if (!W) {
                X = z(G.parentNode);
                if (!X.spmId) {
                    u(G);
                    return
                }
                m(G, X);
                W = h.tryToGetAttribute(G, K)
            }
            C(G, W)
        },
        c = function(Y) {
            if (!Y || Y.nodeType != 1) {
                return
            }
            h.tryToRemoveAttribute(Y, "data-spm-max-idx");
            var T = h.nodeListToArray(Y.getElementsByTagName("a")),
            X = h.nodeListToArray(Y.getElementsByTagName("area")),
            Z = T.concat(X),
            W,
            G = Z.length;
            for (W = 0; W < G; W++) {
                h.tryToRemoveAttribute(Z[W], K)
            }
        },
        N = function(T) {
            var W = T.tagName,
            G;
            if (W != "A" && W != "AREA") {
                return ""
            }
            y(T);
            G = h.tryToGetAttribute(T, K);
            return G ? G: ""
        },
        S = function() {
            e(function() {
                o = v;
                if (!w()) {
                    return
                }
                Q();
                h.on(l.body, "mousedown",
                function(W, T) {
                    var G;
                    while (T && (G = T.tagName.toLowerCase())) {
                        if (G === "a" || G === "area") {
                            y(T);
                            break
                        } else {
                            if (G === "body" || G === "html") {
                                break
                            }
                        }
                        T = T.parentNode
                    }
                })
            });
            P.g_SPM = {
                resetModule: c,
                anchorBeacon: y,
                getParam: N
            }
        };
        return {
            init: S
        }
    })
} (MAGNETO)); (function(a) {
    a.moduleManager.register("essential",
    function() {
        var i = this,
        p = a.globals,
        n = i.moduleManager,
        f = i.tools,
        c = i.config,
        d = n.require("cookieProcessor"),
        o = n.require("spm"),
        g = n.require("recorder"),
        k = n.require("ua"),
        l = p.customize,
        h = function() {
            var r, s = d.get("__cn_logon__") === "true";
            return s
        },
        m = function() {
            var r = p.win.dmtrack_c;
            if (!r || r === "{-}") {
                return {}
            }
            r = r.substring(1, r.length - 1).replace(/ali_resin_trace=/, "");
            return f.parseParam(r, "|")
        },
        e = function() {
            try {
                var t = f.getReferrer(),
                u = f.random(),
                r = l.acookieAdditional || {},
                s = {
                    cache: u,
                    pre: t
                };
                g.sendEssentialInfo(c.acookieSever, {},
                f.combineJson(s, r))
            } catch(v) {
                f.sendErrorInfo(v, "acookie")
            }
        },
        b = function() {
            var u = k.extraBrowser,
            r = u.name + u.ver.toFixed(1),
            s = k.system.name,
            t = r + "|" + s + "|" + k.resolution + "|" + k.language;
            return t
        },
        j = function(w) {
            var u = l.needCookies,
            t = c.needDefaultCookies,
            r, s, v = "-";
            if (f.isArray(t) && u != undefined) {
                t = t.concat(u)
            }
            r = t.length;
            while (r--) {
                s = t[r];
                v = d.get(s) || "-";
                w[s] = v
            }
        },
        q = function() {
            if (!f.sampling()) {
                return
            }
            try {
                o.init();
                var w = encodeURI(f.getReferrer()),
                u = d.getSubCookies("ali_apache_track") || {},
                t = c.logSeverOne,
                v = m(),
                s = d.getSubCookies("aliBeacon_bcookie") || {},
                r = encodeURI(p.doc.location.href);
                if (c.isSetCookieToAcookie) {
                    e()
                }
                j(u);
                if (c.isCheckLogin && v.c_signed == undefined) {
                    v.c_signed = h() ? 1 : 0
                }
                f.combineJson(v, s, true);
                d.remove("aliBeacon_bcookie");
                g.sendEssentialInfo(t, {
                    p: "{" + c.siteNo + "}",
                    u: "{" + f.trimHttpStr(r) + "}",
                    m: "{GET}",
                    s: "{200}",
                    r: "{" + w + "}",
                    a: "{" + f.combineParam(u, {},
                    "|") + "}",
                    b: "{-}",
                    c: "{" + f.combineParam(v, s, "|", true) + "}"
                },
                {
                    pageid: f.randomPageId(),
                    sys: b()
                })
            } catch(x) {
                f.sendErrorInfo(x, "essential")
            }
        };
        return {
            init: q
        }
    },
    true)
})(MAGNETO); (function(b) {
    var e = b.globals,
    d = e.doc,
    a = b.tools,
    g = b.config,
    h = b.moduleManager,
    c = h.require("recorder"),
    f = h.require("cookieProcessor");
    b.api = {
        log: function(j, n) {
            try {
                var m = {},
                k = {},
                i = j.split("?");
                if (i[1] !== undefined) {
                    k = a.parseParam(i[1], "&")
                }
                if (a.isString(n)) {
                    if (n.substring(0, 1) === "?") {
                        n = n.substring(1)
                    }
                    m = a.parseParam(n, "&")
                } else {
                    if (a.is(n, Object)) {
                        m = n
                    }
                }
                m.st_page_id = e.pageId;
                c.sendEssentialInfo(i[0], {},
                a.combineJson(m, k))
            } catch(l) {
                a.sendErrorInfo(l, "log")
            }
        },
        asysLog: function(i, j, l) {
            try {
                if (!j || j === "-") {
                    j = d.location.href
                }
                c.sendEssentialInfo(g.logSeverTwo, {
                    p: "{" + g.siteNo + "}",
                    u: "{" + a.trimHttpStr(i) + "}",
                    m: "{GET}",
                    s: "{200}",
                    r: "{" + j + "}",
                    a: "{" + f.get("ali_apache_track") + "}",
                    b: "{-}",
                    c: "{" + a.combineParam(l || {},
                    {},
                    "|") || "-}"
                },
                {
                    pageid: a.randomPageId()
                })
            } catch(k) {
                a.sendErrorInfo(k, "asysLog")
            }
        },
        flashLog: function(j, k) {
            try {
                var i = e.win.dmtrack_c;
                if (!i || i === "{-}") {
                    i = "-"
                } else {
                    i = i.substring(1, i.length - 1).replace(/ali_resin_trace=/, "")
                }
                if (!k || k === "-") {
                    k = d.location.href
                }
                c.sendEssentialInfo(g.logSeverTwo, {
                    p: "{" + g.siteNo + "}",
                    u: "{" + j + "}",
                    m: "{GET}",
                    s: "{200}",
                    r: "{" + k + "}",
                    a: "{" + f.get("ali_apache_track") + "}",
                    b: "{-}",
                    c: "{" + i + "}"
                },
                {
                    pageid: a.randomPageId(),
                    dmtrack_type: "xuanwangpu"
                })
            } catch(l) {
                a.sendErrorInfo(l, "asysLog")
            }
        }
    }
})(MAGNETO); (function(b) {
    var d = b.globals,
    c = d.win,
    e = b.config,
    a = b.api;
    c.sk_dmtracking = function() {
        if (d.isConflicted === true) {
            return
        }
        b.moduleManager.require("essential").init()
    };
    c.dmtrack = {
        clickstat: function(f, g) {
            a.log(f, g)
        },
        tracelog: function(f) {
            a.log(e.tracelogSever, {
                tracelog: f
            })
        },
        beacon_click: function(f, g, h) {
            a.asysLog(f, g, h)
        },
        flash_dmtracking: function(f, g) {
            a.flashLog(f, g)
        }
    }
})(MAGNETO);