YAHOO.namespace("TB.app.Survey"); (function() {
    var textareaLen = 1000,
    inputLen = 70;
    YAHOO.lang.augmentObject(TB.app.Survey, {
        init: function() {
            if ($D.get("submitForm")) {
                $E.on($D.get("submitForm"), "click",
                function(e) {
                    var flag = this.beAnsweredQuestion.init();
                    if (!flag || !(TB.app.Survey.isFileValid.inValidFileNumber() == 0)) {
                        $E.preventDefault(e)
                    }
                    TB.app.Survey.submitForm()
                },
                this, this)
            }
            this.msgText.init();
            this.bgColors();
            this.theOtherBox.init();
            this.imgOption.init();
            this.remarkQustion.init();
            this.timeSelect.init();
            this.cal.init()
        },
        progress: function(currentPage, totalPage) {
            var percent = Math.floor(currentPage / totalPage * 100);
            var bars = $D.getElementsByClassName("percent-bar", "div");
            var span = $D.getElementsByClassName("percent", "span");
            for (var i = 0,
            len = bars.length; i < len; i++) {
                $D.setStyle(bars[i], "width", percent + "%");
                span[i].innerHTML = percent
            }
        },
        bgColors: function() {
            var rootNode = $D.getElementsByClassName("question-wrap")[0];
            var labels = rootNode.getElementsByTagName("label");
            this.method = function(e) {
                $E.on(e, "mouseover",
                function() {
                    $D.addClass(e, "ac")
                },
                e);
                $E.on(e, "mouseout",
                function() {
                    $D.removeClass(e, "ac")
                },
                e);
                if (YAHOO.env.ua.ie === 6) {
                    $E.on(e, "click",
                    function(ev, el) {
                        var els = el.getElementsByTagName("input");
                        if (els.length) {
                            els[0].click();
                            if ($D.hasClass(els[0], "time")) {
                                els[0].focus()
                            }
                        }
                    },
                    e)
                }
            };
            $D.batch(labels, this.method)
        },
        msgText: {
            init: function() {
                var textereas = $D.getElementsByClassName("text-input", "", "question-wrap");
                var textinput = $D.getElementsByClassName("text", "input", "question-wrap");
                var textinput1 = $D.getElementsByClassName("remark", "input", "question-wrap");
                textereas = textereas.concat(textinput, textinput1);
                for (var i = 0,
                len = textereas.length; i < len; i++) {
                    $E.on(textereas[i], "focus", this.focusFunc, textereas[i], this);
                    $E.on(textereas[i], "keyup", this.keyupFunc, textereas[i], this)
                }
            },
            CheckStringLength: function(txt) {
                var len;
                len = 0;
                for (var i = 0; i < txt.length; i++) {
                    if (txt.charCodeAt(i) >= 19968 && txt.charCodeAt(i) <= 40869) {
                        len += 2
                    } else {
                        len += 1
                    }
                }
                return len
            },
            getMsg: function(obj, classname) {
                var ansistor = $D.getAncestorByClassName(obj, "question-content");
                var alertMsg = $D.getElementBy(function(el) {
                    if ($D.hasClass(el, "msg") && $D.getElementsByClassName(classname, "p", el).length) {
                        return true
                    }
                },
                "div", ansistor);
                return alertMsg
            },
            keyupFunc: function(e, obj) {
                var oNum = $D.hasClass(obj, "J_InputText") ? textareaLen * 2 : inputLen * 2;
                var overLength = this.CheckStringLength(YAHOO.lang.trim(obj.value)) - oNum;
                var errMsg = this.getMsg(obj, "error");
                if (!errMsg.getElementsByTagName) {
                    return
                }
                var spanEle = errMsg.getElementsByTagName("span");
                var atteionMsg = this.getMsg(obj, "attention");
                if (overLength > 0) {
                    $D.setStyle(atteionMsg, "display", "none");
                    $D.setStyle(errMsg, "display", "block");
                    spanEle[0].innerHTML = overLength;
                    TB.app.Survey.beAnsweredQuestion.fontLong = false
                } else {
                    $D.setStyle(errMsg, "display", "none");
                    TB.app.Survey.beAnsweredQuestion.fontLong = true
                }
            },
            blurFunc: function(e, obj) {
                var atteionMsg = this.getMsg(obj, "attention");
                $D.setStyle(atteionMsg, "display", "none")
            },
            focusFunc: function(e, obj) {
                var atteionMsg = this.getMsg(obj, "attention");
                var errMsg = this.getMsg(obj, "error");
                if (errMsg.style.display === "none") {
                    $D.setStyle(atteionMsg, "display", "block");
                    var p = atteionMsg.getElementsByTagName("p")[0];
                    var oNum = $D.hasClass(obj, "J_InputText") ? textareaLen: inputLen;
                    p.innerHTML = "\u60a8\u6700\u591a\u53ef\u4ee5\u8f93\u5165" + oNum + "\u5b57\u3002"
                }
                this.keyupFunc(e, obj)
            }
        },
        theOtherBox: {
            otherBox: function() {
                return $D.getElementsByClassName("other", "", "content")
            },
            radioOtherBox: function(obj) {
                if (obj[0].type.toLocaleLowerCase() == "radio") {
                    var Ancestor = $D.getAncestorByClassName(obj[0], "question-content");
                    var sibling = $D.getElementsBy(function(el) {
                        if (el.type.toLocaleLowerCase() == "radio" && !$D.getAncestorByClassName(el, "other")) {
                            return true
                        }
                    },
                    "input", Ancestor);
                    var msgs = $D.getElementsByClassName("msg", "div", $D.getAncestorByClassName(obj[0], "question-item"));
                    for (var i = 0; i < sibling.length; i++) {
                        $E.on(sibling[i], "click",
                        function(el) {
                            $D.addClass(obj[1], "input-disable");
                            obj[1].disabled = true;
                            $D.batch(msgs,
                            function(msg) {
                                msg.style.display = "none"
                            },
                            this, this)
                        })
                    }
                }
            },
            checkOtherBox: function(obj) {
                if (obj[0].type.toLocaleLowerCase() == "checkbox") {
                    obj[1].disabled = true;
                    $D.addClass(obj[1], "input-disable")
                }
            },
            toggleBoxInput: function(e, obj) {
                if (obj[0].checked) {
                    obj[1].disabled = false;
                    $D.removeClass(obj[1], "input-disable");
                    obj[1].focus();
                    this.radioOtherBox(obj)
                } else {
                    this.checkOtherBox(obj);
                    var msgs = $D.getElementsByClassName("msg", "div", $D.getAncestorByClassName(obj[0], "question-item"));
                    $D.batch(msgs,
                    function(msg) {
                        msg.style.display = "none"
                    })
                }
            },
            init: function() {
                var otherBox = this.otherBox();
                for (var i = 0,
                len = otherBox.length; i < len; i++) {
                    var otherBoxInput = otherBox[i].getElementsByTagName("input");
                    if (otherBoxInput.length > 1) {
                        $E.on(otherBoxInput[0], "click", this.toggleBoxInput, otherBoxInput, this)
                    }
                }
            }
        },
        getCheckbox: function(inputNUM, boxType) {
            var box = [];
            for (var i = 0; i < inputNUM.length; i++) {
                if (inputNUM[i].type.toLocaleLowerCase() == boxType) {
                    box.push(inputNUM[i])
                }
            }
            return (box)
        },
        isFileValid: {
            fileList: [],
            fileState: [],
            addFile: function(objId) {
                var len = this.fileList.length;
                for (var i = 0; i < len; i++) {
                    if (this.fileList[i] == objId) {
                        return
                    }
                }
                this.fileList[len] = objId;
                this.fileState[len] = true
            },
            inValidFileNumber: function() {
                var len = this.fileList.length;
                var count = 0;
                for (var i = 0; i < len; i++) {
                    if (this.fileState[i] == false) {
                        count++
                    }
                }
                return count
            },
            setState: function(objId, state) {
                var len = this.fileList.length;
                for (var i = 0; i < len; i++) {
                    if (this.fileList[i] == objId) {
                        this.fileState[i] = state
                    }
                }
            },
            checkFile: function(objId) {
                this.addFile(objId);
                var inputs = TB.app.Survey.beAnsweredQuestion.getElements(objId, "input");
                if (inputs[0].type.toLocaleLowerCase() != "file") {
                    return
                }
                var path = inputs[0].value;
                var successHandle = function(o) {
                    var result = YAHOO.lang.JSON.parse(o.responseText);
                    if (result.isSuccess === "F") {
                        var err = $D.getElementsByClassName("file-check", "div", objId);
                        var span = $D.getElementsByClassName("err-msg", "span", objId);
                        span[0].innerHTML = result.errMsg;
                        $D.setStyle(err, "display", "block");
                        TB.app.Survey.isFileValid.setState(objId, false)
                    } else {
                        var err = $D.getElementsByClassName("file-check", "div", objId);
                        $D.setStyle(err, "display", "none");
                        TB.app.Survey.isFileValid.setState(objId, true)
                    }
                };
                var failureHandle = function(o) {
                    alert("\u7f51\u7edc\u9519\u8bef")
                };
                var callback = {
                    success: successHandle,
                    failure: failureHandle,
                    argument: objId
                };
                YAHOO.util.Connect.asyncRequest("post", "checkFile.do", callback, "path=" + path)
            }
        },
        beAnsweredQuestion: {
            container: null,
            ansQuewstions: [],
            QuewstionArr: [],
            flag: true,
            fontLong: true,
            isorder: true,
            getQuewstionsID: function() {
                for (var i = 0,
                len = this.ansQuewstions.length; i < len; i++) {
                    var ansQuewstionID = $D.getAncestorByClassName(this.ansQuewstions[i], "question-item");
                    this.QuewstionArr.push(ansQuewstionID)
                }
            },
            getElements: function(objID, tagName) {
                return ($D.getElementsBy(function(el) {
                    return true
                },
                tagName, objID))
            },
            getElementsType: function(objID) {
                if (this.getElements(objID, "select").length > 0) {
                    return ("select")
                } else {
                    if (this.getElements(objID, "textarea").length > 0) {
                        return ("textarea")
                    } else {
                        if (this.getElements(objID, "input").length > 0) {
                            return ("input")
                        }
                    }
                }
            },
            selectQuestion: function(objID) {
                var selectArr = this.getElements(objID, "select");
                var err = $D.getElementsByClassName("must-msg", "div", objID);
                for (var i = 0,
                len = selectArr.length; i < len; i++) {
                    if (selectArr[i].selectedIndex === 0) {
                        this.flag = false;
                        $D.setStyle(err, "display", "block");
                        return
                    }
                    $D.setStyle(err, "display", "none")
                }
            },
            textAreaQuestion: function(objID) {
                var textArea = this.getElements(objID, "textarea")[0];
                var selectArr = this.getElements(objID, "select");
                var err = $D.getElementsByClassName("must-msg", "div", objID);
                if (YAHOO.lang.trim(textArea.value).length === 0) {
                    this.flag = false;
                    $D.setStyle(err, "display", "block");
                    return
                }
                $D.setStyle(err, "display", "none")
            },
            checkboxRadio: function(inputs) {
                var num = 0;
                var objID = $D.getAncestorByClassName(inputs[0], "question-item");
                var selectArr = this.getElements(objID, "select");
                var err = $D.getElementsByClassName("must-msg", "div", objID);
                for (var i = 0,
                len = inputs.length; i < len; i++) {
                    if (inputs[i].checked) {
                        num++;
                        continue
                    }
                }
                if (num == 0) {
                    this.flag = false;
                    $D.setStyle(err, "display", "block");
                    return
                }
                $D.setStyle(err, "display", "none")
            },
            matrix: function(table) {
                var objID = $D.getAncestorByClassName(table, "question-item");
                var selectArr = this.getElements(objID, "select");
                var err = $D.getElementsByClassName("must-msg", "div", objID);
                for (var i = 1,
                len = table.rows.length; i < len; i++) {
                    var num = 0;
                    for (var j = 1,
                    len1 = table.rows[i].cells.length; j < len1; j++) {
                        var input_c = $D.getElementBy(function(el) {
                            if (el.type.toLocaleLowerCase() != "text") {
                                return true
                            }
                        },
                        "input", table.rows[i].cells[j]);
                        if (input_c.checked) {
                            num++
                        }
                    }
                    if (num === 0) {
                        this.flag = false;
                        $D.setStyle(err, "display", "block");
                        return
                    }
                    $D.setStyle(err, "display", "none")
                }
            },
            inputQuestion: function(objID) {
                var inputs = this.getElements(objID, "input");
                if (inputs[0].type.toLocaleLowerCase() == "text" || inputs[0].type.toLocaleLowerCase() == "file") {
                    var err = $D.getElementsByClassName("must-msg", "div", objID);
                    if (inputs.length == 1 && inputs[0].value.length === 0) {
                        this.flag = false;
                        $D.setStyle(err, "display", "block");
                        return
                    }
                    $D.setStyle(err, "display", "none")
                } else {
                    var tableSquare = $D.getElementsBy(function(el) {
                        if ($D.hasClass(el, "table-square")) {
                            return true
                        }
                    },
                    "table", objID);
                    tableSquare.length > 0 ? this.matrix(tableSquare[0]) : this.checkboxRadio(inputs)
                }
            },
            showErr: function() {
                $D.setStyle($D.get("nextPageInfo"), "display", "block")
            },
            hideErr: function() {
                $D.setStyle($D.get("nextPageInfo"), "display", "none")
            },
            checkOrder: function() {
                var orderList = $D.getElementsByClassName("order-question", "div", "question-wrap");
                if (!orderList.length) {
                    return true
                }
                $D.batch(orderList,
                function(elcontainer) {
                    var orderselect = $D.getElementsByClassName("order", "select", elcontainer);
                    var orderstat = true;
                    var orderindex = 0;
                    for (var i = 0,
                    len = orderselect.length; i < len; i++) {
                        if (orderselect[i].selectedIndex == 0) {
                            orderstat = false;
                            continue
                        }
                        orderindex = orderindex + parseInt(orderselect[i].selectedIndex)
                    }
                    if (!orderstat && orderindex > 0) {
                        $D.getElementsByClassName("error", "p", "nextPageInfo")[0].innerHTML = "\u60a8\u7684\u6392\u5e8f\u9898\u672a\u6392\u5b8c\uff0c\u8bf7\u6392\u5e8f\u5b8c\u6bd5\u518d\u63d0\u4ea4.";
                        TB.app.Survey.beAnsweredQuestion.showErr();
                        TB.app.Survey.beAnsweredQuestion.isorder = false
                    } else {
                        TB.app.Survey.beAnsweredQuestion.isorder = true
                    }
                })
            },
            checkFontinput: function() {
                var errMsg = $D.getElementsBy(function(el) {
                    if ($D.hasClass(el, "msg") && $D.getElementsByClassName("error", "p", el).length && el.style.display !== "none") {
                        return true
                    }
                },
                "div", "question-wrap");
                if (errMsg.length) {
                    $D.getElementsByClassName("error", "p", "nextPageInfo")[0].innerHTML = "\u6240\u586b\u5199\u6587\u5b57\u592a\u957f\uff0c\u8bf7\u68c0\u67e5.";
                    this.showErr();
                    return false
                } else {
                    return true
                }
            },
            init: function() {
                if (!this.checkFontinput()) {
                    return
                }
                this.checkOrder();
                if (!this.isorder) {
                    return
                }
                this.hideErr();
                $D.getElementsByClassName("error", "p", "nextPageInfo")[0].innerHTML = "\u60a8\u6709\u5fc5\u7b54\u9898\u672a\u586b\u5199\uff0c\u4e0d\u80fd\u8fdb\u5165\u4e0b\u4e00\u9875\uff01";
                this.flag = true;
                this.container = $D.get("question-wrap");
                this.ansQuewstions = $D.getElementsBy(function(el) {
                    if ($D.hasClass(el, "must-answer") && $D.getAncestorByClassName(el, "question-item").style.display != "none") {
                        return true
                    }
                },
                "sup", this.container);
                this.getQuewstionsID();
                for (var i = 0,
                len = this.QuewstionArr.length; i < len; i++) {
                    var elementType = this.getElementsType(this.QuewstionArr[i]);
                    switch (elementType) {
                    case "select":
                        this.selectQuestion(this.QuewstionArr[i]);
                        break;
                    case "textarea":
                        this.textAreaQuestion(this.QuewstionArr[i]);
                        break;
                    case "input":
                        this.inputQuestion(this.QuewstionArr[i]);
                        break
                    }
                }
                if (!this.flag) {
                    this.showErr();
                    return false
                }
                return true
            }
        },
        imgOption: {
            container: null,
            imgsOption: null,
            imgOther: function(ele) {
                var otherbox = $D.getElementBy(function(el) {
                    if ($D.getAncestorByClassName(el, "other") && el.type.toLocaleLowerCase() == "radio") {
                        return true
                    }
                },
                "input", ele);
                if (otherbox.length == 0) {
                    return
                }
                $E.on(otherbox, "click",
                function() {
                    var selectedImg = $D.getElementsByClassName("selected-img", "img", ele);
                    $D.removeClass(selectedImg, "selected-img")
                })
            },
            imgOtherbox: function() {
                var imgContainer = $D.getElementsByClassName("img-question", "div", this.container);
                $D.batch(imgContainer, this.imgOther)
            },
            imgClickOptionSingle: function(e, i) {
                var imgContainer = $D.getAncestorByClassName(this.imgsOption[i], "img-question");
                var imgsGroup = $D.getElementsBy(function(el) {
                    return true
                },
                "img", imgContainer);
                $D.removeClass(imgsGroup, "selected-img");
                $D.addClass(this.imgsOption[i], "selected-img");
                var target = $E.getTarget(e);
                if (target.tagName === "IMG") {
                    $D.getPreviousSibling(this.imgsOption[i]).click()
                }
                $D.getAncestorByTagName(this.imgsOption[i], "a").blur()
            },
            imgClickOptionMulti: function(e, i) {
                var imgContainer = $D.getAncestorByClassName(this.imgsOption[i], "img-question");
                var imgsGroup = $D.getElementsBy(function(el) {
                    return true
                },
                "img", imgContainer);
                var target = $E.getTarget(e);
                if (target.tagName === "IMG") {
                    $D.getPreviousSibling(this.imgsOption[i]).click()
                } else {
                    if (!$D.getPreviousSibling(this.imgsOption[i]).checked) {
                        $D.removeClass(this.imgsOption[i], "selected-img")
                    } else {
                        $D.addClass(this.imgsOption[i], "selected-img")
                    }
                }
                $D.getAncestorByTagName(this.imgsOption[i], "a").blur()
            },
            init: function() {
                this.container = $D.get("question-wrap");
                this.imgsOption = $D.getElementsBy(function(el) {
                    if ($D.getAncestorByClassName(el, "img-option")) {
                        return true
                    }
                },
                "img", this.container);
                if (!this.imgsOption.length) {
                    return
                }
                for (var i = 0; i < this.imgsOption.length; i++) {
                    var inputBoxType = $D.getPreviousSibling(this.imgsOption[i]).type.toLocaleLowerCase();
                    var sibling = $D.getPreviousSibling(this.imgsOption[i]);
                    if (inputBoxType == "radio") {
                        $E.on([sibling, this.imgsOption[i]], "click", this.imgClickOptionSingle, i, this)
                    } else {
                        if (inputBoxType == "checkbox") {
                            $E.on([sibling, this.imgsOption[i]], "click", this.imgClickOptionMulti, i, this)
                        }
                    }
                }
                this.imgOtherbox()
            }
        },
        remarkQustion: {
            btnRemark: function(wrap) {
                return ($D.getElementsBy(function(el) {
                    if (el.type.toLocaleLowerCase() != "text") {
                        return true
                    }
                },
                "input", wrap))
            },
            textRemark: function(wrap) {
                return ($D.getElementsBy(function(el) {
                    if (el.type.toLocaleLowerCase() == "text") {
                        return true
                    }
                },
                "input", wrap))
            },
            isAbled: function(inputTxt) {
                $D.removeClass(inputTxt, "disable");
                inputTxt.disabled = false
            },
            unAbled: function(inputTxt) {
                $D.addClass(inputTxt, "disable");
                inputTxt.disabled = true
            },
            radioRemark: function(e, opt) {
                if (opt.radio.checked) {
                    for (var i = 0,
                    len = opt.inputTxt.length; i < len; i++) {
                        if (opt.order != i) {
                            this.unAbled(opt.inputTxt[i])
                        }
                    }
                    this.isAbled(opt.inputTxt[opt.order])
                }
            },
            checkboxRemark: function(e, opt) {
                if (opt.checkbox.checked) {
                    this.isAbled(opt.inputTxt[opt.order])
                } else {
                    this.unAbled(opt.inputTxt[opt.order])
                }
            },
            radioEvent: function(remark, remarkInput) {
                for (var i = 0,
                len = remark.length; i < len; i++) {
                    $E.on(remark[i], "click", this.radioRemark, {
                        radio: remark[i],
                        inputTxt: remarkInput,
                        order: i
                    },
                    this)
                }
            },
            checkboxEvent: function(remark, remarkInput) {
                for (var i = 0,
                len = remark.length; i < len; i++) {
                    $E.on(remark[i], "click", this.checkboxRemark, {
                        checkbox: remark[i],
                        inputTxt: remarkInput,
                        order: i
                    },
                    this)
                }
            },
            addEvents: function(wrap) {
                var remark = this.btnRemark(wrap);
                var remarkInput = this.textRemark(wrap);
                if (!remark[0]) {
                    return
                }
                if (remark[0].type.toLocaleLowerCase() == "radio") {
                    this.radioEvent(remark, remarkInput)
                } else {
                    this.checkboxEvent(remark, remarkInput)
                }
            },
            init: function() {
                this.remarkInputWrap = $D.getElementsByClassName("table-question", "table", $D.get("question-wrap"));
                for (var i = 0,
                len = this.remarkInputWrap.length; i < len; i++) {
                    this.addEvents(this.remarkInputWrap[i])
                }
            }
        },
        timeSelect: {
            MonHead: [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
            findSelect: function(e, clsName) {
                if (e.type.toLocaleLowerCase() == "select") {
                    return true
                }
            },
            writeMonth: function(el) {
                for (var i = 1; i <= 12; i++) {
                    el.options.add(new Option(i, i))
                }
            },
            writeDay: function(dd, n) {
                this.optionsClear(dd);
                for (var i = 1; i < (n + 1); i++) {
                    dd.options.add(new Option(i, i))
                }
            },
            IsPinYear: function(year) {
                return (0 == year % 4 && (year % 100 != 0 || year % 400 == 0))
            },
            optionsClear: function(e) {
                e.options.length = 1
            },
            YYYYDD: function(e, el) {
                var mm = $D.getNextSiblingBy(el,
                function(e) {
                    if ($D.hasClass(e, "time-mm")) {
                        return true
                    }
                });
                var dd = $D.getNextSiblingBy(mm,
                function(e) {
                    if ($D.hasClass(e, "time-dd")) {
                        return true
                    }
                });
                if (el.selectedIndex == 0) {
                    this.optionsClear(mm);
                    this.optionsClear(dd);
                    return
                }
                if (mm.selectedIndex == 0) {
                    this.writeMonth(mm)
                }
                if (mm.selectedIndex == 2) {
                    this.IsPinYear(el.value) ? this.writeDay(dd, 29) : this.writeDay(dd, 28)
                }
            },
            MMDD: function(e, el) {
                var yy = $D.getPreviousSiblingBy(el,
                function(e) {
                    if ($D.hasClass(e, "time-yy")) {
                        return true
                    }
                });
                var dd = $D.getNextSiblingBy(yy,
                function(e) {
                    if ($D.hasClass(e, "time-dd")) {
                        return true
                    }
                });
                if (el.selectedIndex == 0) {
                    this.optionsClear(dd);
                    return
                }
                this.IsPinYear(yy.value) && el.selectedIndex == 2 ? this.writeDay(dd, 29) : this.writeDay(dd, this.MonHead[el.selectedIndex - 1])
            },
            addEventer: function(el) {
                var mm = $D.getNextSiblingBy(el,
                function(e) {
                    if ($D.hasClass(e, "time-mm")) {
                        return true
                    }
                });
                $E.on(el, "change", TB.app.Survey.timeSelect.YYYYDD, el, TB.app.Survey.timeSelect);
                $E.on(mm, "change", TB.app.Survey.timeSelect.MMDD, mm, TB.app.Survey.timeSelect)
            },
            init: function() {
                selectTime = $D.getElementsByClassName("time-yy", "select", "question-wrap");
                $D.batch(selectTime, this.addEventer)
            }
        },
        cal: {
            cal: [],
            cals: null,
            calader: function(i) {
                var id = $D.getAttribute($D.getAncestorByClassName(this.cals[i], "question-item"), "id");
                this.cal[i] = TB.widget.SimpleCalendar.init(this.cals[i], null, null, {
                    footer: '<button type="button" onclick="TB.app.Survey.cal.cals[' + i + "].value = ''\" id=\"" + id + '_reset">\u7f6e\u7a7a</button> <button onclick="TB.app.Survey.cal.cal[' + i + '].select(new Date());" id="' + id + '_today">\u4eca\u5929</button>'
                })
            },
            init: function() {
                this.cals = $D.getElementsByClassName("time", "input", "question-wrap");
                for (var i = 0,
                len = this.cals.length; i < len; i++) {
                    this.calader(i);
                    this.cals[i].onfocus = function(e) {
                        this.blur()
                    };
                    if (YAHOO.env.ua.ie === 6) {
                        $E.on(this.cals[i], "click",
                        function(e) {
                            $E.stopEvent(e)
                        })
                    }
                }
            }
        }
    });
    TB.app.Survey.CheckboxValid = function(arr, elementID) {
        var inputNum = $D.getElementsBy(function(el) {
            if (el.type.toLocaleLowerCase() == "checkbox") {
                return true
            }
        },
        "input", $D.get(elementID));
        var arrNum;
        var msgBox = $D.getElementBy(function(el) {
            if ($D.hasClass(el, "err-msg")) {
                return true
            }
        },
        "div", elementID);
        var checkboxArr = [];
        this.setOtherBox = function(j) {
            $D.setStyle(msgBox, "display", "block");
            for (var i = 0; i < arr.length; i++) {
                if (i == j) {
                    continue
                } else {
                    for (var n = 0,
                    len = arr[i].length; n < len; n++) {
                        var parentEle = $D.getAncestorByTagName($D.get(arr[i][n]), "label");
                        $D.addClass(parentEle, "unable");
                        $D.get(arr[i][n]).disabled = true;
                        arrNum = j
                    }
                }
            }
        };
        this.cancelBox = function(e, j) {
            if (arrNum == j) {
                var stat = false;
                for (var i = 0,
                len = arr[arrNum].length; i < len; i++) {
                    stat = $D.get(arr[arrNum][i]).checked || stat
                }
                if (!stat) {
                    $D.setStyle(msgBox, "display", "none");
                    for (var n = 0; n < arr.length; n++) {
                        if (n == j) {
                            continue
                        }
                        for (var m = 0; m < arr[n].length; m++) {
                            var parentEle = $D.getAncestorByTagName($D.get(arr[n][m]), "label");
                            $D.removeClass(parentEle, "unable");
                            $D.get(arr[n][m]).disabled = false
                        }
                    }
                    arrNum = null
                }
                return
            }
            this.setOtherBox(j)
        };
        this.init = function() {
            checkboxArr = TB.app.Survey.getCheckbox(inputNum, "checkbox");
            for (var j = 0; j < arr.length; j++) {
                for (var n = 0,
                len = arr[j].length; n < len; n++) {
                    var curBox = $D.get(arr[j][n]);
                    $E.on(curBox, "click", this.cancelBox, j, this)
                }
            }
        };
        this.init()
    };
    TB.app.Survey.OrderList = function(wrapID) {
        var preIndex = [];
        var selectList = document.getElementById(wrapID).getElementsByTagName("select");
        var selectOption = $D.getElementsByClassName("select-option", "div", wrapID);
        this.selectRange = function(e, j) {
            if (this.selectedIndex == 0 && preIndex[j] != 0) {
                for (var n = 0; n < selectList.length; n++) {
                    $D.removeClass(selectList[n].options[preIndex[j]], "unable");
                    if (document.all) {
                        selectList[n].options[preIndex[j]].style.color = "#333333"
                    }
                }
            } else {
                for (var n = 0; n < selectList.length; n++) {
                    for (var i = 0; i < preIndex.length; i++) {
                        if (preIndex[i] == this.selectedIndex) {
                            preIndex[j] > 0 ? this.selectedIndex = preIndex[j] : this.selectedIndex = 0;
                            return
                        }
                    }
                    if (document.all) {
                        selectList[n].options[this.selectedIndex].style.color = "#999999";
                        selectList[n].options[preIndex[j]].style.color = "#333333";
                        continue
                    }
                    $D.addClass(selectList[n].options[this.selectedIndex], "unable");
                    $D.removeClass(selectList[n].options[preIndex[j]], "unable")
                }
            }
            preIndex[j] = selectList[j].selectedIndex
        };
        this.reOrder = function(e, btn) {
            for (var i = 0,
            len = selectList.length; i < len; i++) {
                selectList[i].selectedIndex = 0;
                for (var j = 0,
                len1 = preIndex.length; j < len1; j++) {
                    var opt = selectList[i].options[preIndex[j]];
                    if (document.all) {
                        opt.style.color = "#000000";
                        continue
                    }
                    $D.removeClass(opt, "unable")
                }
            }
            for (var i = 0,
            len1 = preIndex.length; i < len1; i++) {
                preIndex[i] = 0
            }
            btn.blur()
        };
        this.reOrderBtnShow = function() {
            var reOrderBtn = $D.getElementBy(function(el) {
                return true
            },
            "button", wrapID);
            $E.on(reOrderBtn, "click", this.reOrder, reOrderBtn, this)
        };
        this.init = function() {
            for (var i = 0; i < selectList.length; i++) {
                preIndex[i] = selectList[i].selectedIndex;
                $E.on(selectList[i], "change", this.selectRange, i, selectList[i])
            }
        };
        this.init();
        this.reOrderBtnShow()
    };
    TB.app.Survey.ReductQuestion = function(questionName) {
        var question = $D.getElementsBy(function(el) {
            var name = $D.getAttribute(el, "name");
            if (name == questionName) {
                return true
            }
        },
        "div", "question-wrap");
        this.nextEleCheck = function(nextEle, j) {
            $D.setStyle(nextEle, "display", "block");
            var _inputNum = nextEle.getElementsByTagName("input");
            var _checkboxArr = TB.app.Survey.getCheckbox(_inputNum, "checkbox");
            _checkboxArr[j].disabled = false;
            $D.removeClass($D.getAncestorByTagName(_checkboxArr[j], "div"), "unable")
        };
        this.nextEleCancelCheck = function(j, m) {
            for (var i = m + 1; i < question.length; i++) {
                var _inputNum = question[i].getElementsByTagName("input");
                var _checkboxArr = TB.app.Survey.getCheckbox(_inputNum, "checkbox");
                _checkboxArr[j].disabled = true;
                _checkboxArr[j].checked = false;
                $D.addClass($D.getAncestorByTagName(_checkboxArr[j], "div"), "unable");
                this.nextEleHidden(question[i], i);
                var Ancestor = $D.getAncestorByTagName(_inputNum[j], "div");
                if ($D.hasClass(Ancestor, "other")) {
                    var otherinput = $D.getElementsByClassName("text", "input", Ancestor)[0];
                    $D.addClass(otherinput, "input-disable");
                    otherinput.disabled = true
                }
            }
        };
        this.nextEleHidden = function(Ele, m) {
            var _checkNum = 0;
            var _inputNumc = Ele.getElementsByTagName("input");
            var _checkboxArrc = TB.app.Survey.getCheckbox(_inputNumc, "checkbox");
            for (i = 0; i < _checkboxArrc.length; i++) {
                if (_checkboxArrc[i].checked) {
                    _checkNum++
                }
            }
            if (_checkNum == 0) {
                for (var i = m + 1; i < question.length; i++) {
                    var _inputNum = question[i].getElementsByTagName("input");
                    var _checkboxArr = TB.app.Survey.getCheckbox(inputNum, "checkbox");
                    $D.setStyle(question[i], "display", "none")
                }
            }
        };
        this.nextQuestion = function(e, o) {
            var Ele = $D.getAncestorByClassName(o.obj, "question-item");
            var nextEle = $D.getNextSibling(Ele);
            if (nextEle.getAttribute("name") != questionName) {
                return
            }
            if (o.obj.checked) {
                this.nextEleCheck(nextEle, o.j)
            } else {
                this.nextEleCancelCheck(o.j, o.i);
                this.nextEleHidden(Ele, o.i)
            }
        };
        for (var i = 0; i < question.length; i++) {
            var inputNum = question[i].getElementsByTagName("input");
            var checkboxArr = TB.app.Survey.getCheckbox(inputNum, "checkbox");
            for (var j = 0; j < checkboxArr.length; j++) {
                $E.on(checkboxArr[j], "click", this.nextQuestion, {
                    j: j,
                    i: i,
                    obj: checkboxArr[j]
                },
                this)
            }
        }
    };
    TB.app.Survey.RedirectQuestion = function(questionID, opt) {
        var inputNum = $D.get(questionID).getElementsByTagName("input");
        var radios = TB.app.Survey.getCheckbox(inputNum, "radio");
        this.nextObj = $D.getElementsByClassName("hidden_info", "input", questionID)[0];
        this.getNextRedirect = function(obj) {
            var nextDirect = $D.getElementsByClassName("hidden_info", "input", obj)[0];
            if (!nextDirect) {
                $D.setStyle($D.get(obj), "display", "none");
                return
            }
            if (nextDirect.value) {
                this.getNextRedirect(nextDirect.value);
                $D.setStyle($D.get(nextDirect.value), "display", "none");
                $D.setStyle($D.get(obj), "display", "none")
            } else {
                $D.setStyle($D.get(obj), "display", "none");
                this.nextObj.value = ""
            }
        };
        this.ElementHidden = function(obj) {
            $D.setStyle($D.get(obj), "display", "none");
            this.getNextRedirect(obj)
        };
        this.ElementShow = function(obj) {
            $D.setStyle($D.get(obj), "display", "block")
        };
        this.redirectTo = function(e, i) {
            if (this.nextObj.value && this.nextObj.value != opt[i][1]) {
                this.getNextRedirect(this.nextObj.value)
            }
            this.ElementShow(opt[i][1]);
            this.nextObj.value = opt[i][1]
        };
        this.cancelQuestion = function() {
            if (this.nextObj.value) {
                this.getNextRedirect(this.nextObj.value)
            }
        };
        this.unDirectOptions = function() {
            for (var i = 0,
            len = radios.length; i < len; i++) {
                $E.on(radios[i], "click", this.cancelQuestion, this, this)
            }
        };
        this.init = function() {
            this.nextObj.value = "";
            this.unDirectOptions();
            for (var i = 0,
            len = opt.length; i < len; i++) {
                $E.removeListener($D.get(opt[i][0]));
                $E.on($D.get(opt[i][0]), "click", this.redirectTo, i, this)
            }
        };
        this.init()
    };
    TB.app.Survey.requestUrl = null;
    TB.app.Survey.RedirectImprove = function() {
        var allAswer;
        var agentClick = function(e) {
            var target = $E.getTarget(e);
            if (target.tagName.toLocaleLowerCase() === "input" || target.tagName.toLocaleLowerCase() == "select") {
                $E.stopPropagation(e);
                var ansistor = $D.getAncestorByClassName(target, "question-item");
                allAswer = [];
                var data = $D.getAttribute(ansistor, "data");
                if (!data || !data.length) {
                    return
                }
                var objStrArr = {
                    sID: null,
                    aimQus: [],
                    allAswers: []
                };
                objStrArr.sID = $D.get("sid").value;
                var quesIDs = data.split(",");
                $D.batch(quesIDs,
                function(ques) {
                    if (!ques) {
                        return
                    }
                    objStrArr.aimQus.push(ques.id);
                    quesAnser(ques)
                });
                var callback = {
                    success: successHanddle,
                    failure: failureHanddle,
                    argument: {
                        quesID: ""
                    }
                };
                objStrArr.allAswers = objStrArr.allAswers.concat(allAswer);
                var anserArrStr = YAHOO.lang.JSON.stringify(objStrArr, "object", 20);
                var connect = YAHOO.util.Connect.asyncRequest("post", TB.app.Survey.requestUrl, callback, "anserArrStr=" + anserArrStr)
            }
        };
        var questionValueSet = function(quesID) {
            var els = $D.getElementsBy(function(el) {
                if (el.tagName == "INPUT" && el.type.toLocaleLowerCase() != "text") {
                    return true
                }
            },
            "input", quesID);
            if (els.length == 0) {
                els = $D.getElementsBy(function(el) {
                    if (el.tagName == "OPTION") {
                        return true
                    }
                },
                "option", quesID)
            }
            var valueSet = new Array;
            for (var i = 0,
            el; el = els[i++];) {
                if (el.checked || el.selected) {
                    valueSet.push(el.value)
                }
            }
            return valueSet
        };
        var getPrevData = function(qID) {
            var prevDataHidden = $D.get("prevQuestionSet");
            var a = new Function("return" + prevDataHidden.value);
            var prevData = a();
            for (var i = 0,
            ques; ques = prevData[i++];) {
                if (ques.quesID === qID) {
                    return ques.answer
                }
            }
        };
        var quesAnser = function(ques) {
            var str = $D.getAttribute(ques, "dataset");
            if (!str) {
                return
            }
            var quesSet = str.split(",");
            var quesAnserSet = [];
            for (var i = 0,
            len = quesSet.length; i < len; i++) {
                quesID = quesSet[i];
                var isExst = false;
                for (var n = 0,
                len1 = allAswer.length; n < len1; n++) {
                    if (quesID === allAswer[n].quesID) {
                        isExst = true;
                        continue
                    }
                }
                if (isExst) {
                    continue
                }
                var singelQues = {};
                singelQues.quesID = quesID;
                singelQues.answer = $D.get(quesID) ? questionValueSet(quesID) : getPrevData(quesID);
                allAswer.push(singelQues)
            }
        };
        var successHanddle = function(o) {
            var resultsText = YAHOO.lang.JSON.parse(o.responseText);
            if (resultsText.isSuccess === "T") {
                results = resultsText.result;
                for (var i = 0,
                len = results.length; i < len; i++) {
                    $D.setStyle(results[i].qus, "display", results[i].display);
                    var question_content;
                    if (document.all) {
                        for (var k = 0; k < $D.get(results[i].qus).children.length; k++) {
                            if ($D.get(results[i].qus).children[k].className.indexOf("question-content") > -1) {
                                question_content = $D.get(results[i].qus).children[k]
                            }
                        }
                        for (var j = 0,
                        length = question_content.children.length; j < length; j++) {
                            var disable;
                            if (results[i].display == "none") {
                                disable = true
                            } else {
                                disable = null
                            }
                            var inputs = question_content.getElementsByTagName("input");
                            for (var ii = 0; ii < inputs.length; ii++) {
                                inputs[ii].disabled = disable
                            }
                            var selects = question_content.getElementsByTagName("select");
                            for (var ii = 0; ii < selects.length; ii++) {
                                selects[ii].disabled = disable
                            }
                            var textareas = question_content.getElementsByTagName("textarea");
                            for (var ii = 0; ii < textareas.length; ii++) {
                                textareas[ii].disabled = disable
                            }
                        }
                    } else {
                        var disable;
                        if (results[i].display == "none") {
                            disable = true
                        } else {
                            disable = null
                        }
                        var inputs = $D.get(results[i].qus).getElementsByTagName("input");
                        for (var ii = 0; ii < inputs.length; ii++) {
                            inputs[ii].disabled = disable
                        }
                        var selects = $D.get(results[i].qus).getElementsByTagName("select");
                        for (var ii = 0; ii < selects.length; ii++) {
                            selects[ii].disabled = disable
                        }
                        var textareas = $D.get(results[i].qus).getElementsByTagName("textarea");
                        for (var ii = 0; ii < textareas.length; ii++) {
                            textareas[ii].disabled = disable
                        }
                    }
                }
            } else {
                if (resultsText.isSuccess === "F") {}
            }
        };
        var failureHanddle = function() {
            alert("\u7f51\u7edc\u9519\u8bef")
        };
        if ($D.get("question-wrap").getElementsByTagName("select").length > 0) {
            $E.on($D.get("question-wrap").getElementsByTagName("select"), "change", agentClick, this, this);
            $E.on($D.get("question-wrap").getElementsByTagName("input"), "click", agentClick, this, this)
        } else {
            $E.on("question-wrap", "click", agentClick, this, this)
        }
    };
    TB.app.Survey.submitForm = function() {
        var allData = (function() {
            var data = $D.getElementsBy(function(el) {
                if ($D.hasClass(el, "question-item") && $D.getAttribute(el, "data")) {
                    return true
                }
            },
            "div", "question-wrap");
            return data
        })();
        var dataArr = [];
        var questionValueSet = function(quesID) {
            var els = $D.getElementsBy(function(el) {
                if (el.tagName == "INPUT" && el.type.toLocaleLowerCase() != "text") {
                    return true
                }
            },
            "input", quesID);
            var valueSet = new Array;
            for (var i = 0,
            el; el = els[i++];) {
                if (el.checked) {
                    valueSet.push(el.value)
                }
            }
            return valueSet
        };
        $D.batch(allData,
        function(data) {
            var quesArr = {};
            quesArr.quesID = data.id;
            quesArr.answer = questionValueSet(data.id);
            dataArr.push(quesArr)
        });
        var prevDataHidden = eval($D.get("prevQuestionSet").value.trim());
        if (prevDataHidden && prevDataHidden.length) {
            dataArr = dataArr.concat(prevDataHidden)
        }
        $D.get("allQuestionSet").value = YAHOO.lang.JSON.stringify(dataArr, "object", 10)
    }
})();
$E.onDOMReady(function() {
    var A = function(I) {
        var B = $D.getAncestorByClassName(I, "question-item");
        var E = Number($D.getAttribute(B, "maxcheckedbox"));
        if (E) {
            var C = $D.getElementsByClassName("table-square", "", B);
            if (C && C.length) {
                B = $D.getAncestorByTagName(I, "tr")
            }
            var D = 0;
            var G = $D.getElementsBy(function(J) {
                if (J.type.toLocaleLowerCase() == "checkbox") {
                    return true
                }
            },
            "input", B);
            if (!G) {
                return
            }
            var H = [];
            $D.batch(G,
            function(J) {
                if (J.checked) {
                    D++
                } else {
                    if (J !== I) {
                        H.push(J)
                    }
                }
            });
            var F;
            if (D >= E) {
                F = true
            } else {
                F = false
            }
            $D.batch(H,
            function(J) {
                var K = J.parentNode;
                if (!$D.hasClass(K, "unable")) {
                    J.disabled = F
                }
            })
        }
    };
    $E.on("question-wrap", "click",
    function(B) {
        var C = $E.getTarget(B);
        if (C.type && C.type.toLocaleLowerCase() == "checkbox") {
            A(C)
        }
    });
    TB.app.Survey.init();
    TB.app.Survey.RedirectImprove()
});