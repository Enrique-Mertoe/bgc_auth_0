!function (w, f) {
    f(w);
}(window, function (w) {
    let smv = {
        init: () => {
            smv.auth()
            smv.events()
        },
        auth() {
            if (!$(".auth-container").length) return;

            const submit = form => {
                let btn = $(form).find(".form-submit");
                btn.addClass("submitting")
            }
            const un_submit = form => {
                let btn = $(form).find(".form-submit");
                btn.removeClass("submitting")
            }
            $$(document).on("submit", ".auth-forms form:not(.form-groupy)", function (ev) {
                ev.preventDefault();
                let _self = this, ep = 0;
                $(this).find("[name]").each(function (ev) {
                    if (!this.value.trim().length)
                        ep++
                });

                const msg = (message) => {
                    $$(_self).find(".smv-form-errors ").show().find("span").txt(message);
                }

                if (ep) return msg("All fields required!");
                submit(this)
                let tgt = $(this).data("u-target");
                tgt = tgt ? "&target=" + tgt : "";

                let url = $$(this).data("action") || "/xhr/auth?step=" + $(this).data("step");
                $.post(url,
                    $(_self).serialize() + tgt
                ).then(res => {
                    un_submit(_self);
                    if (res.is_reset) {
                        if (res.ok) {
                            location.href = res.rdr || "/auth/login"
                        } else {
                            alert(res.data)
                        }
                        return
                    }
                    if (res.ok) {

                        if (res.finish)
                            location.href = "/"
                        $$(".auth-forms").html(res.data);
                    } else {
                        alert(res.data)
                    }
                });
            });


            $$(document).on("submit", ".form-groupy", function (ev) {
                ev.preventDefault();
                let form = $$(this),
                    _self = this,
                    msg = form.find(".smv-form-errors").hide(),
                    btn = SMV.btn_loader(form.find("[type=submit]"));

                function addMessage(message, suc) {
                    if (!msg.size) return;
                    if (suc)
                        msg.aClass("smv-success")
                    msg.show().find("span").txt(message)
                }

                if (SMV.is_form_empty(this)) {
                    addMessage("All fields required.")
                    return
                }
                let step = $$(this).data("form-step");
                if (!step)
                    $$(this).data("form-step", 1) && (() => {
                        step = 1;
                    })();
                btn.load();
                let data = $$(this).data("form-data");
                let d1 = $(this).serialize();
                if (form.data("can_send")) {
                    data += "&" + d1;
                    $.post({
                        url: SMV.smv_url(form.attr("action")),
                        data: data
                    }).then(res => {
                        btn.dismiss();
                        if (res.error) return addMessage(res.error);
                        if (res.ok) {
                            location.href = res.rdr || "/"
                        } else {
                            addMessage(res.data)
                        }
                    })
                    return;
                }

                $.post(
                    {
                        url: SMV.smv_url("xhr/form_register?step=" + $$(this).data("form-step")),
                        data: d1
                    }
                ).then(res => {
                    btn.dismiss();
                    if (res.error) return addMessage(res.error);
                    if (res.can_send) {
                        form.data("can_send", !0);
                    }
                    if (res.ok) {
                        form.find(".smv-groupy-content").html(res.data);
                        form.data("form-step", step + 1);

                        if (!data) {
                            data = d1
                            $$(_self).data("form-data", data);
                        } else {
                            data += "&" + d1;
                            $$(_self).data("form-data", data);
                        }
                    }
                }).catch(res => {
                    console.log(res);
                })


            }).on("click", ".smv-password-toggle", function (ev) {
                ev.preventDefault();
                let inp = $$(this).next();
                let type = inp.attr("type") === "password" ? "text" : "password";
                inp.attr("type", type);
            })
        },
        events() {
            SMV.on("page-change", function (ev) {
                // ev.preventDefault()
            });
            $$(document).on("click", "[data-form-edit-btn]", function (ev) {
                ev.preventDefault();
                alert()
            });
        },

    }
    smv.init();
});