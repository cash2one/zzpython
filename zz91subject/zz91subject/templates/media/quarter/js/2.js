document.write('<link rel="stylesheet" type="text/css" href="' + TB.env.yuipath + 'build/calendar/assets/calendar.css" />');
document.write('<script src="' + TB.env.yuipath + 'build/calendar/calendar-min.js" type="text/javascript"><\/script>');
TB.widget.SimpleCalendar = new
function() {
    var e = YAHOO.util,
    h = e.Dom,
    n = e.Event,
    j = e.Lang;
    var i = [".yui-calcontainer { z-index: 99; }", ".yui-calendar {font-family: verdana !important;}", ".yui-calendar td.calcell.previous {text-decoration: line-through;}", ".yui-calendar td.calcell.oom a {color: #ccc !important;}", ".yui-calendar select.calyearselector, .yui-calendar select.calmonthselector {height: 18px;	line-height: 18px; font-size: 11px; font-family: verdana;}", ".yui-calcontainer .yui-cal-nav, .yui-calcontainer .yui-cal-nav-b button {font-size: 100% !important;}", ".yui-calendar tfoot td {padding-top: 3px;}"];
    TB.dom.addCSS(i.join(""));
    var k = {
        DATE_FIELD_DELIMITER: "-",
        DATE_RANGE_DELIMITER: "~",
        MDY_YEAR_POSITION: 1,
        MDY_MONTH_POSITION: 2,
        MDY_DAY_POSITION: 3,
        MY_YEAR_POSITION: 1,
        MY_MONTH_POSITION: 2,
        MONTHS_SHORT: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        MONTHS_LONG: ["1\u6708", "2\u6708", "3\u6708", "4\u6708", "5\u6708", "6\u6708", "7\u6708", "8\u6708", "9\u6708", "10\u6708", "11\u6708", "12\u6708"],
        WEEKDAYS_1CHAR: ["\u65e5", "\u4e00", "\u4e8c", "\u4e09", "\u56db", "\u4e94", "\u516d"],
        WEEKDAYS_SHORT: ["\u65e5", "\u4e00", "\u4e8c", "\u4e09", "\u56db", "\u4e94", "\u516d"],
        WEEKDAYS_MEDIUM: ["\u65e5", "\u4e00", "\u4e8c", "\u4e09", "\u56db", "\u4e94", "\u516d"],
        WEEKDAYS_LONG: ["\u65e5", "\u4e00", "\u4e8c", "\u4e09", "\u56db", "\u4e94", "\u516d"],
        MY_LABEL_YEAR_POSITION: 1,
        MY_LABEL_MONTH_POSITION: 2,
        MY_LABEL_YEAR_SUFFIX: "\u5e74",
        MY_LABEL_MONTH_SUFFIX: "\u6708",
        LOCALE_MONTHS: "short"
    };
    var g = {
        strings: {
            month: "\u9009\u62e9\u6708\u4efd",
            year: "\u8f93\u5165\u5e74\u4efd",
            submit: "\u786e\u5b9a",
            cancel: "\u53d6\u6d88",
            invalidYear: "\u8bf7\u8f93\u5165\u6709\u6548\u7684\u5e74\u4efd"
        },
        initialFocus: "year"
    };
    var m = {
        YEAR_MAX: 2020,
        YEAR_MIN: 1970
    };
    var d = function(o) {
        return ((o < 10) ? "0": "") + o
    };
    var c = function() {
        this[this._status == "show" ? "hide": "show"]()
    };
    var b = function(q, p) {
        var o = document.createElement("div");
        o.id = q + "_container";
        return (h.get(p) || document.body).appendChild(o)
    };
    var l = function() {
        var o = /^(\d{4})-(?:[0]?)(\d{1,2})-(?:[0]?)(\d{1,2})$/;
        return function(r) {
            try {
                var p = r.match(o).slice(1);
                return new Date(p[0], p[1] - 1, p[2])
            } catch(q) {
                return r
            }
        }
    } ();
    var a = function(p) {
        if (j.isString(p)) {
            if (p.indexOf("-") != -1) {
                return p
            }
            if ("today" == p.toLowerCase()) {
                var o = new Date();
                return f([o.getFullYear(), o.getMonth() + 1, o.getDate()])
            }
        } else {
            if (j.isArray(p)) {
                return f(p)
            }
        }
    };
    var f = function(o) {
        return o[0] + "-" + d(o[1]) + "-" + d(o[2])
    };
    return {
        config_zh: k,
        enhance: function(p, o) {
            o = j.merge(m, o || {});
            if (o.maxdate) {
                o.maxdate = a(o.maxdate);
                p.cfg.setProperty("maxdate", o.maxdate)
            }
            if (o.mindate) {
                o.mindate = a(o.mindate);
                p.cfg.setProperty("mindate", o.mindate)
            }
            if (o.selected) {
                o.selected = a(o.selected);
                p.cfg.setProperty("pagedate", l(o.selected));
                p.cfg.setProperty("selected", o.selected)
            }
            if (o.enableOOM) {
                p.renderCellNotThisMonth = function(r, q) {
                    h.addClass(q, this.Style.CSS_CELL_OOM);
                    q.innerHTML = r.getDate();
                    return p.renderCellDefault(r, q)
                }
            }
            if (!o.pages && o.enableSelectYear) {
                p.buildMonthLabel = function() {
                    var s = this.cfg.getProperty(YAHOO.widget.Calendar._DEFAULT_CONFIG.PAGEDATE.key);
                    var w = s.getFullYear(),
                    r = s.getMonth();
                    var t = ['<select class="calyearselector">'];
                    for (var v = o.YEAR_MIN; v <= o.YEAR_MAX; ++v) {
                        t.push('<option value="' + v + '"' + (w == v ? ' selected="selected"': "") + ">" + v + "</option>")
                    }
                    t.push("</select>");
                    var u = ['<select class="calmonthselector">'];
                    for (var q = 0; q < 12; ++q) {
                        u.push('<option value="' + q + '"' + (r == q ? ' selected="selected"': "") + ">" + (q + 1) + "</option>")
                    }
                    u.push("</select>");
                    return t.join("") + this.Locale.MY_LABEL_YEAR_SUFFIX + u.join("") + this.Locale.MY_LABEL_MONTH_SUFFIX
                };
                p.renderEvent.subscribe(function() {
                    var r = this.cfg.getProperty(YAHOO.widget.Calendar._DEFAULT_CONFIG.PAGEDATE.key);
                    var s = r.getFullYear(),
                    t = r.getMonth();
                    if (s == o.YEAR_MAX && t == 11 && this.linkRight) {
                        h.setStyle(this.linkRight, "display", "none")
                    } else {
                        if (s == o.YEAR_MIN && t == 0 && this.linkLeft) {
                            h.setStyle(this.linkLeft, "display", "none")
                        }
                    }
                    var q = this.oDomContainer.getElementsByTagName("select");
                    n.on(q[0], "change",
                    function(u, v) {
                        v.setYear(this.value);
                        v.render()
                    },
                    this);
                    n.on(q[1], "change",
                    function(u, v) {
                        v.setMonth(this.value);
                        v.render()
                    },
                    this)
                },
                p, true)
            }
        },
        init: function(q, p, o, r) {
            p = h.get(p);
            q = h.get(q);
            o = h.get(o) || q;
            r = r || {};
            var t = h.generateId(null, "_tbpc_");
            if (!p) {
                p = b(t, r.containerRoot)
            }
            var v;
            if (r.navigator) {
                if (j.isObject(r.navigator)) {
                    j.augmentObject(r.navigator, g)
                } else {
                    r.navigator = g
                }
            }
            if (r.pages && r.pages > 1) {
                v = new YAHOO.widget.CalendarGroup(t, p.id, j.merge(k, r))
            } else {
                v = new YAHOO.widget.Calendar(t, p.id, j.merge(k, r))
            }
            this.enhance(v, r);
            if (j.isFunction(r.onSelect)) {
                v.selectEvent.subscribe(r.onSelect, v, true)
            }
            if (j.isFunction(r.onBeforeSelect)) {
                v.beforeSelectEvent.subscribe(r.onBeforeSelect, v, true)
            }
            if (j.isFunction(r.onClear)) {
                v.clearEvent.subscribe(r.onClear, v, true)
            }
            if (r.footer) {
                v.renderFooter = function(w) {
                    w.push('<tfoot><tr><td colspan="8">' + r.footer + "</td></tr></tfoot>");
                    return w
                }
            }
            var s = function(y, w, z) {
                var x = w[0];
                q.value = f(x[0]);
                u.hide()
            };
            h.setStyle(p, "position", "absolute");
            v.selectEvent.subscribe(s, v, true);
            v.hide();
            v.render();
            var u = {};
            u._status = "hide";
            u._beforeShowEvent = new e.CustomEvent("beforeShow", u, false, e.CustomEvent.FLAT);
            u.calObj = v;
            u.hide = function() {
                v.hide();
                u._status = "hide"
            };
            u.show = function() {
                u._beforeShowEvent.fire();
                v.show();
                u._status = "show";
                var w = h.getXY(q);
                w[1] += q.offsetHeight;
                h.setXY(p, w)
            };
            u.select = function(w) {
                return v.select(w)
            };
            u.getSelectedDates = function() {
                return v.getSelectedDates()
            };
            n.on(o, (q === o) ? "focus": "click", c, u, true);
            n.on(document, "mousedown",
            function(w) {
                var x = n.getTarget(w);
                if (! (x === q || x === o || h.isAncestor(p, x))) {
                    u.hide()
                }
            });
            n.on(document, "keydown",
            function(w) {
                if (w.keyCode == 27) {
                    u.hide()
                }
            });
            return u
        },
        initRange: function(o, t, s, q) {
            if (!j.isArray(o) || o.length < 2) {
                alert("You need pass an array including tow input fields.");
                return
            }
            var r = this.init(o[0], t ? t[0] : null, s ? toogles[0] : null, q);
            var u = this.init(o[1], t ? t[1] : null, s ? toogles[1] : null, q);
            var p = function() {
                var A = arguments[1][0],
                v = arguments[1][1],
                x = this._input.value,
                z = A._input.value;
                A.hide();
                var w = this.calObj.cfg,
                y = false;
                if (x && w.getProperty("selected") == "") {
                    this.calObj.cfg.setProperty("pagedate", l(x));
                    this.calObj.cfg.setProperty("selected", x);
                    y = true
                }
                if (z) {
                    if (!x) {
                        this.calObj.cfg.setProperty("pagedate", l(z))
                    }
                    this.calObj.cfg.setProperty(v == 1 ? "mindate": "maxdate", z);
                    y = true
                }
                if (y) {
                    this.calObj.render()
                }
            };
            r._beforeShowEvent.subscribe(p, [u, 0], r);
            r._input = o[0];
            u._beforeShowEvent.subscribe(p, [r, 1], u);
            u._input = o[1];
            if (q.autoMoveToNext) {
                r.calObj.selectEvent.subscribe(function() {
                    if (u._input.value == "" && !u._input.disabled) {
                        u.show()
                    }
                })
            }
            return [r, u]
        }
    }
};