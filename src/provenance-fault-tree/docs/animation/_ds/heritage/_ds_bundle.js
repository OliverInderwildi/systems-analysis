/* @ds-bundle: {"format":4,"namespace":"HeritageDesignSystem_ffe1f3","components":[{"name":"Badge","sourcePath":"components/core/Badge.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"Card","sourcePath":"components/core/Card.jsx"},{"name":"IconButton","sourcePath":"components/core/IconButton.jsx"},{"name":"Tag","sourcePath":"components/core/Tag.jsx"},{"name":"Alert","sourcePath":"components/feedback/Alert.jsx"},{"name":"Dialog","sourcePath":"components/feedback/Dialog.jsx"},{"name":"Tooltip","sourcePath":"components/feedback/Tooltip.jsx"},{"name":"Checkbox","sourcePath":"components/forms/Checkbox.jsx"},{"name":"Input","sourcePath":"components/forms/Input.jsx"},{"name":"Radio","sourcePath":"components/forms/Radio.jsx"},{"name":"Select","sourcePath":"components/forms/Select.jsx"},{"name":"Switch","sourcePath":"components/forms/Switch.jsx"},{"name":"Tabs","sourcePath":"components/navigation/Tabs.jsx"}],"sourceHashes":{"components/core/Badge.jsx":"ec8086c22827","components/core/Button.jsx":"98577810e7f9","components/core/Card.jsx":"067b0429c6c3","components/core/IconButton.jsx":"620b837058e9","components/core/Tag.jsx":"bf814747a3f0","components/feedback/Alert.jsx":"d5f0a08a42e8","components/feedback/Dialog.jsx":"34213084399d","components/feedback/Tooltip.jsx":"76835fe2c749","components/forms/Checkbox.jsx":"7fc758d86c9c","components/forms/Input.jsx":"3a7f7a69ee4d","components/forms/Radio.jsx":"4a0e55743ec4","components/forms/Select.jsx":"d61dcb80088a","components/forms/Switch.jsx":"071cf85f31d5","components/navigation/Tabs.jsx":"7c142dbe283c","ui_kits/showroom/Dashboard.jsx":"ab7a1606b8e1","ui_kits/showroom/Icons.jsx":"d8a8cf32a2e7","ui_kits/showroom/Inventory.jsx":"8156a564d6a5","ui_kits/showroom/Shell.jsx":"b68fa0de4179","ui_kits/showroom/VehicleDetail.jsx":"b187b0379391"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.HeritageDesignSystem_ffe1f3 = window.HeritageDesignSystem_ffe1f3 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/core/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const tones = {
  neutral: {
    bg: "var(--surface-sunken)",
    fg: "var(--text-muted)",
    bd: "var(--border-default)"
  },
  primary: {
    bg: "var(--info-bg)",
    fg: "var(--oxford-blue)",
    bd: "var(--info-border)"
  },
  success: {
    bg: "var(--success-bg)",
    fg: "var(--success)",
    bd: "var(--success-border)"
  },
  warning: {
    bg: "var(--warning-bg)",
    fg: "var(--warning)",
    bd: "var(--warning-border)"
  },
  danger: {
    bg: "var(--danger-bg)",
    fg: "var(--dark-red)",
    bd: "var(--danger-border)"
  },
  gold: {
    bg: "var(--surface-tint-warm)",
    fg: "#8A5A2B",
    bd: "#E4D3BC"
  }
};

/**
 * Badge — a small status/count marker.
 */
function Badge({
  children,
  tone = "neutral",
  solid = false,
  dot = false,
  style = {},
  ...rest
}) {
  const t = tones[tone] || tones.neutral;
  const solidStyle = {
    background: t.fg,
    color: "var(--white)",
    border: "1px solid " + t.fg
  };
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: "6px",
      padding: "2px 9px",
      fontFamily: "var(--font-heading)",
      fontWeight: "var(--fw-medium)",
      fontSize: "var(--text-xs)",
      lineHeight: 1.5,
      letterSpacing: "var(--tracking-wide)",
      borderRadius: "var(--radius-pill)",
      background: solid ? solidStyle.background : t.bg,
      color: solid ? solidStyle.color : t.fg,
      border: solid ? solidStyle.border : "1px solid " + t.bd,
      ...style
    }
  }, rest), dot && /*#__PURE__*/React.createElement("span", {
    style: {
      width: "6px",
      height: "6px",
      borderRadius: "50%",
      background: solid ? "var(--white)" : t.fg
    }
  }), children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Badge.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const sizes = {
  sm: {
    padding: "6px 12px",
    fontSize: "var(--text-sm)",
    height: "32px"
  },
  md: {
    padding: "9px 18px",
    fontSize: "var(--text-base)",
    height: "40px"
  },
  lg: {
    padding: "12px 24px",
    fontSize: "var(--text-lg)",
    height: "48px"
  }
};
const variants = {
  primary: {
    background: "var(--brand-primary)",
    color: "var(--text-inverse)",
    border: "1px solid var(--brand-primary)"
  },
  secondary: {
    background: "var(--surface-card)",
    color: "var(--brand-primary)",
    border: "1px solid var(--border-strong)"
  },
  accent: {
    background: "var(--brand-accent)",
    color: "var(--text-on-accent)",
    border: "1px solid var(--brand-accent)"
  },
  ghost: {
    background: "transparent",
    color: "var(--brand-primary)",
    border: "1px solid transparent"
  },
  danger: {
    background: "var(--danger-strong)",
    color: "var(--text-inverse)",
    border: "1px solid var(--danger-strong)"
  }
};

/**
 * Button — primary interactive control for the Heritage system.
 */
function Button({
  children,
  variant = "primary",
  size = "md",
  disabled = false,
  fullWidth = false,
  iconLeft = null,
  iconRight = null,
  type = "button",
  onClick,
  style = {},
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  const [active, setActive] = React.useState(false);
  const v = variants[variant] || variants.primary;
  const s = sizes[size] || sizes.md;
  const hoverShift = variant === "ghost" ? {
    background: "var(--surface-sunken)"
  } : variant === "secondary" ? {
    background: "var(--surface-sunken)",
    borderColor: "var(--border-strong)"
  } : {
    filter: "brightness(0.92)"
  };
  return /*#__PURE__*/React.createElement("button", _extends({
    type: type,
    disabled: disabled,
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => {
      setHover(false);
      setActive(false);
    },
    onMouseDown: () => setActive(true),
    onMouseUp: () => setActive(false),
    style: {
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      gap: "8px",
      width: fullWidth ? "100%" : "auto",
      height: s.height,
      padding: s.padding,
      fontFamily: "var(--font-heading)",
      fontWeight: "var(--fw-medium)",
      fontSize: s.fontSize,
      lineHeight: 1,
      letterSpacing: "var(--tracking-normal)",
      borderRadius: "var(--radius-sm)",
      cursor: disabled ? "not-allowed" : "pointer",
      opacity: disabled ? 0.45 : 1,
      transition: "background var(--dur-fast) var(--ease-standard), filter var(--dur-fast) var(--ease-standard), transform var(--dur-fast) var(--ease-standard), box-shadow var(--dur-fast) var(--ease-standard)",
      transform: active && !disabled ? "translateY(1px)" : "translateY(0)",
      boxShadow: active ? "none" : "var(--shadow-xs)",
      ...v,
      ...(hover && !disabled ? hoverShift : {}),
      ...style
    }
  }, rest), iconLeft, children, iconRight);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const pads = {
  sm: "var(--space-4)",
  md: "var(--space-6)",
  lg: "var(--space-7)"
};

/**
 * Card — a raised surface container. Hairline border + low cool shadow.
 */
function Card({
  children,
  variant = "default",
  padding = "md",
  interactive = false,
  onClick,
  style = {},
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  const variants = {
    default: {
      background: "var(--surface-card)",
      border: "1px solid var(--border-default)",
      boxShadow: "var(--shadow-sm)"
    },
    flat: {
      background: "var(--surface-card)",
      border: "1px solid var(--border-subtle)",
      boxShadow: "none"
    },
    sunken: {
      background: "var(--surface-sunken)",
      border: "1px solid var(--border-subtle)",
      boxShadow: "none"
    },
    inverse: {
      background: "var(--surface-inverse)",
      border: "1px solid var(--border-inverse)",
      boxShadow: "var(--shadow-md)",
      color: "var(--text-inverse)"
    }
  };
  const v = variants[variant] || variants.default;
  return /*#__PURE__*/React.createElement("div", _extends({
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      borderRadius: "var(--radius-lg)",
      padding: pads[padding] || pads.md,
      transition: "box-shadow var(--dur-base) var(--ease-standard), transform var(--dur-base) var(--ease-standard)",
      cursor: interactive ? "pointer" : "default",
      ...v,
      ...(interactive && hover ? {
        boxShadow: "var(--shadow-lg)",
        transform: "translateY(-2px)"
      } : {}),
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Card.jsx", error: String((e && e.message) || e) }); }

// components/core/IconButton.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const sizes = {
  sm: 32,
  md: 40,
  lg: 48
};
const variants = {
  solid: {
    background: "var(--brand-primary)",
    color: "var(--text-inverse)",
    border: "1px solid var(--brand-primary)"
  },
  outline: {
    background: "var(--surface-card)",
    color: "var(--brand-primary)",
    border: "1px solid var(--border-strong)"
  },
  ghost: {
    background: "transparent",
    color: "var(--brand-primary)",
    border: "1px solid transparent"
  }
};

/**
 * IconButton — a square, icon-only control. Pass a Lucide/SVG icon as children.
 */
function IconButton({
  children,
  variant = "ghost",
  size = "md",
  disabled = false,
  label,
  onClick,
  style = {},
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  const dim = sizes[size] || sizes.md;
  const v = variants[variant] || variants.ghost;
  const hoverShift = variant === "solid" ? {
    filter: "brightness(0.92)"
  } : {
    background: "var(--surface-sunken)"
  };
  return /*#__PURE__*/React.createElement("button", _extends({
    type: "button",
    "aria-label": label,
    title: label,
    disabled: disabled,
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      width: dim + "px",
      height: dim + "px",
      borderRadius: "var(--radius-sm)",
      cursor: disabled ? "not-allowed" : "pointer",
      opacity: disabled ? 0.45 : 1,
      transition: "background var(--dur-fast) var(--ease-standard), filter var(--dur-fast) var(--ease-standard)",
      ...v,
      ...(hover && !disabled ? hoverShift : {}),
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { IconButton });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/IconButton.jsx", error: String((e && e.message) || e) }); }

// components/core/Tag.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Tag — a compact, optionally removable label (e.g. filters, categories).
 */
function Tag({
  children,
  onRemove,
  iconLeft = null,
  style = {},
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: "6px",
      padding: "4px 10px",
      fontFamily: "var(--font-body)",
      fontWeight: "var(--fw-regular)",
      fontSize: "var(--text-sm)",
      lineHeight: 1.4,
      color: "var(--text-body)",
      background: "var(--surface-card)",
      border: "1px solid var(--border-default)",
      borderRadius: "var(--radius-sm)",
      ...style
    }
  }, rest), iconLeft, children, onRemove && /*#__PURE__*/React.createElement("button", {
    type: "button",
    "aria-label": "Remove",
    onClick: onRemove,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      width: "16px",
      height: "16px",
      marginRight: "-2px",
      padding: 0,
      border: "none",
      borderRadius: "var(--radius-xs)",
      cursor: "pointer",
      background: hover ? "var(--surface-sunken)" : "transparent",
      color: "var(--text-muted)",
      fontSize: "13px",
      lineHeight: 1
    }
  }, "\xD7"));
}
Object.assign(__ds_scope, { Tag });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Tag.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Alert.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const tones = {
  info: {
    bg: "var(--info-bg)",
    bd: "var(--info-border)",
    fg: "var(--oxford-blue)",
    accent: "var(--steel-navy)"
  },
  success: {
    bg: "var(--success-bg)",
    bd: "var(--success-border)",
    fg: "#0B341C",
    accent: "var(--success)"
  },
  warning: {
    bg: "var(--warning-bg)",
    bd: "var(--warning-border)",
    fg: "#7A4A00",
    accent: "var(--warning-accent)"
  },
  danger: {
    bg: "var(--danger-bg)",
    bd: "var(--danger-border)",
    fg: "var(--dark-red)",
    accent: "var(--danger)"
  }
};
const glyphs = {
  info: "i",
  success: "✓",
  warning: "!",
  danger: "!"
};

/**
 * Alert — an inline message banner with a leading marker and optional title.
 */
function Alert({
  children,
  tone = "info",
  title,
  onClose,
  style = {},
  ...rest
}) {
  const t = tones[tone] || tones.info;
  return /*#__PURE__*/React.createElement("div", _extends({
    role: "status",
    style: {
      display: "flex",
      gap: "12px",
      alignItems: "flex-start",
      padding: "14px 16px",
      background: t.bg,
      border: "1px solid " + t.bd,
      borderLeft: "3px solid " + t.accent,
      borderRadius: "var(--radius-sm)",
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      width: "20px",
      height: "20px",
      flexShrink: 0,
      marginTop: "1px",
      borderRadius: "50%",
      background: t.accent,
      color: "var(--white)",
      fontFamily: "var(--font-heading)",
      fontWeight: "var(--fw-bold)",
      fontSize: "12px",
      lineHeight: 1
    }
  }, glyphs[tone]), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      minWidth: 0
    }
  }, title && /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: "var(--fw-medium)",
      fontSize: "var(--text-base)",
      color: t.fg,
      marginBottom: children ? "3px" : 0
    }
  }, title), children && /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-body)",
      fontWeight: "var(--fw-light)",
      fontSize: "var(--text-sm)",
      lineHeight: "var(--lh-normal)",
      color: "var(--text-body)"
    }
  }, children)), onClose && /*#__PURE__*/React.createElement("button", {
    type: "button",
    "aria-label": "Dismiss",
    onClick: onClose,
    style: {
      border: "none",
      background: "transparent",
      cursor: "pointer",
      color: t.fg,
      fontSize: "16px",
      lineHeight: 1,
      padding: "2px",
      flexShrink: 0
    }
  }, "\xD7"));
}
Object.assign(__ds_scope, { Alert });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Alert.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Dialog.jsx
try { (() => {
/**
 * Dialog — a centered modal over a scrim. Renders nothing when `open` is false.
 */
function Dialog({
  open,
  onClose,
  title,
  children,
  footer,
  width = 480,
  style = {}
}) {
  React.useEffect(() => {
    if (!open) return;
    const onKey = e => {
      if (e.key === "Escape" && onClose) onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);
  if (!open) return null;
  return /*#__PURE__*/React.createElement("div", {
    onClick: onClose,
    style: {
      position: "fixed",
      inset: 0,
      zIndex: 1000,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      padding: "var(--space-6)",
      background: "rgba(0, 33, 71, 0.42)",
      backdropFilter: "blur(2px)",
      animation: "hds-fade var(--dur-base) var(--ease-standard)"
    }
  }, /*#__PURE__*/React.createElement("style", null, "@keyframes hds-fade{from{opacity:0}to{opacity:1}}@keyframes hds-rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}"), /*#__PURE__*/React.createElement("div", {
    role: "dialog",
    "aria-modal": "true",
    onClick: e => e.stopPropagation(),
    style: {
      width: "100%",
      maxWidth: width + "px",
      background: "var(--surface-card)",
      border: "1px solid var(--border-default)",
      borderRadius: "var(--radius-lg)",
      boxShadow: "var(--shadow-xl)",
      animation: "hds-rise var(--dur-slow) var(--ease-out)",
      overflow: "hidden",
      ...style
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "var(--space-5) var(--space-6)",
      borderBottom: "1px solid var(--border-subtle)"
    }
  }, /*#__PURE__*/React.createElement("h2", {
    style: {
      margin: 0,
      fontFamily: "var(--font-heading)",
      fontWeight: "var(--fw-medium)",
      fontSize: "var(--text-xl)",
      color: "var(--text-strong)"
    }
  }, title), onClose && /*#__PURE__*/React.createElement("button", {
    type: "button",
    "aria-label": "Close",
    onClick: onClose,
    style: {
      border: "none",
      background: "transparent",
      cursor: "pointer",
      color: "var(--text-muted)",
      fontSize: "20px",
      lineHeight: 1,
      padding: "2px"
    }
  }, "\xD7")), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "var(--space-6)",
      fontFamily: "var(--font-body)",
      fontWeight: "var(--fw-light)",
      fontSize: "var(--text-base)",
      lineHeight: "var(--lh-normal)",
      color: "var(--text-body)"
    }
  }, children), footer && /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "flex-end",
      gap: "var(--space-3)",
      padding: "var(--space-4) var(--space-6)",
      borderTop: "1px solid var(--border-subtle)",
      background: "var(--surface-sunken)"
    }
  }, footer)));
}
Object.assign(__ds_scope, { Dialog });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Dialog.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Tooltip.jsx
try { (() => {
/**
 * Tooltip — a small label shown on hover/focus of its child.
 */
function Tooltip({
  children,
  label,
  placement = "top",
  style = {}
}) {
  const [show, setShow] = React.useState(false);
  const pos = {
    top: {
      bottom: "calc(100% + 8px)",
      left: "50%",
      transform: "translateX(-50%)"
    },
    bottom: {
      top: "calc(100% + 8px)",
      left: "50%",
      transform: "translateX(-50%)"
    },
    left: {
      right: "calc(100% + 8px)",
      top: "50%",
      transform: "translateY(-50%)"
    },
    right: {
      left: "calc(100% + 8px)",
      top: "50%",
      transform: "translateY(-50%)"
    }
  };
  return /*#__PURE__*/React.createElement("span", {
    style: {
      position: "relative",
      display: "inline-flex",
      ...style
    },
    onMouseEnter: () => setShow(true),
    onMouseLeave: () => setShow(false),
    onFocus: () => setShow(true),
    onBlur: () => setShow(false)
  }, children, show && /*#__PURE__*/React.createElement("span", {
    role: "tooltip",
    style: {
      position: "absolute",
      zIndex: 900,
      whiteSpace: "nowrap",
      padding: "5px 9px",
      background: "var(--surface-inverse)",
      color: "var(--text-inverse)",
      fontFamily: "var(--font-heading)",
      fontWeight: "var(--fw-medium)",
      fontSize: "var(--text-xs)",
      lineHeight: 1.3,
      borderRadius: "var(--radius-sm)",
      boxShadow: "var(--shadow-md)",
      pointerEvents: "none",
      ...pos[placement]
    }
  }, label));
}
Object.assign(__ds_scope, { Tooltip });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Tooltip.jsx", error: String((e && e.message) || e) }); }

// components/forms/Checkbox.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Checkbox — square check control with label. Controlled via `checked`.
 */
function Checkbox({
  label,
  checked = false,
  onChange,
  disabled = false,
  id,
  style = {},
  ...rest
}) {
  const autoId = React.useId();
  const fieldId = id || autoId;
  return /*#__PURE__*/React.createElement("label", {
    htmlFor: fieldId,
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: "10px",
      cursor: disabled ? "not-allowed" : "pointer",
      opacity: disabled ? 0.55 : 1,
      fontFamily: "var(--font-body)",
      fontWeight: "var(--fw-light)",
      fontSize: "var(--text-base)",
      color: "var(--text-body)",
      ...style
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      width: "18px",
      height: "18px",
      flexShrink: 0,
      borderRadius: "var(--radius-xs)",
      border: "1.5px solid " + (checked ? "var(--brand-primary)" : "var(--border-strong)"),
      background: checked ? "var(--brand-primary)" : "var(--surface-card)",
      transition: "background var(--dur-fast) var(--ease-standard), border-color var(--dur-fast) var(--ease-standard)"
    }
  }, checked && /*#__PURE__*/React.createElement("svg", {
    width: "12",
    height: "12",
    viewBox: "0 0 12 12",
    fill: "none"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M2.5 6.2 L5 8.6 L9.5 3.6",
    stroke: "#fff",
    strokeWidth: "1.8",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }))), /*#__PURE__*/React.createElement("input", _extends({
    id: fieldId,
    type: "checkbox",
    checked: checked,
    disabled: disabled,
    onChange: onChange,
    style: {
      position: "absolute",
      opacity: 0,
      width: 0,
      height: 0
    }
  }, rest)), label);
}
Object.assign(__ds_scope, { Checkbox });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Checkbox.jsx", error: String((e && e.message) || e) }); }

// components/forms/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const sizes = {
  sm: {
    height: "32px",
    padding: "0 10px",
    fontSize: "var(--text-sm)"
  },
  md: {
    height: "40px",
    padding: "0 12px",
    fontSize: "var(--text-base)"
  },
  lg: {
    height: "48px",
    padding: "0 14px",
    fontSize: "var(--text-lg)"
  }
};

/**
 * Input — single-line text field. Supports label, hint, error, adornments.
 */
function Input({
  label,
  hint,
  error,
  size = "md",
  iconLeft = null,
  iconRight = null,
  disabled = false,
  id,
  style = {},
  ...rest
}) {
  const [focus, setFocus] = React.useState(false);
  const s = sizes[size] || sizes.md;
  const autoId = React.useId();
  const fieldId = id || autoId;
  const invalid = Boolean(error);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "6px"
    }
  }, label && /*#__PURE__*/React.createElement("label", {
    htmlFor: fieldId,
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: "var(--fw-medium)",
      fontSize: "var(--text-sm)",
      color: "var(--text-strong)"
    }
  }, label), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: "8px",
      height: s.height,
      padding: s.padding,
      background: disabled ? "var(--surface-sunken)" : "var(--surface-card)",
      border: "1px solid " + (invalid ? "var(--danger)" : focus ? "var(--border-focus)" : "var(--border-default)"),
      borderRadius: "var(--radius-sm)",
      boxShadow: focus ? "var(--ring)" : "none",
      transition: "border-color var(--dur-fast) var(--ease-standard), box-shadow var(--dur-fast) var(--ease-standard)",
      opacity: disabled ? 0.6 : 1,
      ...style
    }
  }, iconLeft && /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      color: "var(--text-subtle)"
    }
  }, iconLeft), /*#__PURE__*/React.createElement("input", _extends({
    id: fieldId,
    disabled: disabled,
    onFocus: () => setFocus(true),
    onBlur: () => setFocus(false),
    style: {
      flex: 1,
      minWidth: 0,
      border: "none",
      outline: "none",
      background: "transparent",
      fontFamily: "var(--font-body)",
      fontWeight: "var(--fw-light)",
      fontSize: s.fontSize,
      color: "var(--text-body)"
    }
  }, rest)), iconRight && /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      color: "var(--text-subtle)"
    }
  }, iconRight)), (hint || error) && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-body)",
      fontSize: "var(--text-xs)",
      color: invalid ? "var(--danger)" : "var(--text-subtle)"
    }
  }, error || hint));
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Input.jsx", error: String((e && e.message) || e) }); }

// components/forms/Radio.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Radio — circular single-choice control with label. Controlled via `checked`.
 */
function Radio({
  label,
  checked = false,
  onChange,
  name,
  value,
  disabled = false,
  id,
  style = {},
  ...rest
}) {
  const autoId = React.useId();
  const fieldId = id || autoId;
  return /*#__PURE__*/React.createElement("label", {
    htmlFor: fieldId,
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: "10px",
      cursor: disabled ? "not-allowed" : "pointer",
      opacity: disabled ? 0.55 : 1,
      fontFamily: "var(--font-body)",
      fontWeight: "var(--fw-light)",
      fontSize: "var(--text-base)",
      color: "var(--text-body)",
      ...style
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      width: "18px",
      height: "18px",
      flexShrink: 0,
      borderRadius: "50%",
      border: "1.5px solid " + (checked ? "var(--brand-primary)" : "var(--border-strong)"),
      background: "var(--surface-card)",
      transition: "border-color var(--dur-fast) var(--ease-standard)"
    }
  }, checked && /*#__PURE__*/React.createElement("span", {
    style: {
      width: "9px",
      height: "9px",
      borderRadius: "50%",
      background: "var(--brand-primary)"
    }
  })), /*#__PURE__*/React.createElement("input", _extends({
    id: fieldId,
    type: "radio",
    name: name,
    value: value,
    checked: checked,
    disabled: disabled,
    onChange: onChange,
    style: {
      position: "absolute",
      opacity: 0,
      width: 0,
      height: 0
    }
  }, rest)), label);
}
Object.assign(__ds_scope, { Radio });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Radio.jsx", error: String((e && e.message) || e) }); }

// components/forms/Select.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const sizes = {
  sm: {
    height: "32px",
    padding: "0 34px 0 10px",
    fontSize: "var(--text-sm)"
  },
  md: {
    height: "40px",
    padding: "0 38px 0 12px",
    fontSize: "var(--text-base)"
  },
  lg: {
    height: "48px",
    padding: "0 42px 0 14px",
    fontSize: "var(--text-lg)"
  }
};

/**
 * Select — native dropdown wrapped to match the Heritage field styling.
 */
function Select({
  label,
  hint,
  error,
  size = "md",
  options = [],
  disabled = false,
  placeholder,
  id,
  style = {},
  ...rest
}) {
  const [focus, setFocus] = React.useState(false);
  const s = sizes[size] || sizes.md;
  const autoId = React.useId();
  const fieldId = id || autoId;
  const invalid = Boolean(error);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "6px"
    }
  }, label && /*#__PURE__*/React.createElement("label", {
    htmlFor: fieldId,
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: "var(--fw-medium)",
      fontSize: "var(--text-sm)",
      color: "var(--text-strong)"
    }
  }, label), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      display: "flex",
      ...style
    }
  }, /*#__PURE__*/React.createElement("select", _extends({
    id: fieldId,
    disabled: disabled,
    onFocus: () => setFocus(true),
    onBlur: () => setFocus(false),
    style: {
      appearance: "none",
      WebkitAppearance: "none",
      width: "100%",
      height: s.height,
      padding: s.padding,
      fontFamily: "var(--font-body)",
      fontWeight: "var(--fw-light)",
      fontSize: s.fontSize,
      color: "var(--text-body)",
      background: disabled ? "var(--surface-sunken)" : "var(--surface-card)",
      border: "1px solid " + (invalid ? "var(--danger)" : focus ? "var(--border-focus)" : "var(--border-default)"),
      borderRadius: "var(--radius-sm)",
      boxShadow: focus ? "var(--ring)" : "none",
      transition: "border-color var(--dur-fast) var(--ease-standard), box-shadow var(--dur-fast) var(--ease-standard)",
      cursor: disabled ? "not-allowed" : "pointer",
      opacity: disabled ? 0.6 : 1
    }
  }, rest), placeholder && /*#__PURE__*/React.createElement("option", {
    value: ""
  }, placeholder), options.map(o => {
    const val = typeof o === "string" ? o : o.value;
    const lbl = typeof o === "string" ? o : o.label;
    return /*#__PURE__*/React.createElement("option", {
      key: val,
      value: val
    }, lbl);
  })), /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      right: "12px",
      top: "50%",
      transform: "translateY(-50%)",
      pointerEvents: "none",
      color: "var(--text-subtle)",
      fontSize: "12px"
    }
  }, "\u25BE")), (hint || error) && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-body)",
      fontSize: "var(--text-xs)",
      color: invalid ? "var(--danger)" : "var(--text-subtle)"
    }
  }, error || hint));
}
Object.assign(__ds_scope, { Select });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Select.jsx", error: String((e && e.message) || e) }); }

// components/forms/Switch.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Switch — a binary toggle. Controlled via `checked`.
 */
function Switch({
  label,
  checked = false,
  onChange,
  disabled = false,
  id,
  style = {},
  ...rest
}) {
  const autoId = React.useId();
  const fieldId = id || autoId;
  return /*#__PURE__*/React.createElement("label", {
    htmlFor: fieldId,
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: "10px",
      cursor: disabled ? "not-allowed" : "pointer",
      opacity: disabled ? 0.55 : 1,
      fontFamily: "var(--font-body)",
      fontWeight: "var(--fw-light)",
      fontSize: "var(--text-base)",
      color: "var(--text-body)",
      ...style
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      position: "relative",
      display: "inline-flex",
      alignItems: "center",
      width: "40px",
      height: "22px",
      flexShrink: 0,
      padding: "2px",
      borderRadius: "var(--radius-pill)",
      background: checked ? "var(--brand-secondary)" : "var(--grey-medium)",
      transition: "background var(--dur-base) var(--ease-standard)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: "18px",
      height: "18px",
      borderRadius: "50%",
      background: "var(--white)",
      boxShadow: "var(--shadow-sm)",
      transform: checked ? "translateX(18px)" : "translateX(0)",
      transition: "transform var(--dur-base) var(--ease-out)"
    }
  })), /*#__PURE__*/React.createElement("input", _extends({
    id: fieldId,
    type: "checkbox",
    role: "switch",
    checked: checked,
    disabled: disabled,
    onChange: onChange,
    style: {
      position: "absolute",
      opacity: 0,
      width: 0,
      height: 0
    }
  }, rest)), label);
}
Object.assign(__ds_scope, { Switch });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Switch.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Tabs.jsx
try { (() => {
/**
 * Tabs — an underline tab strip. Controlled via `value` + `onChange`.
 * `items` is an array of { value, label }.
 */
function Tabs({
  items = [],
  value,
  onChange,
  style = {}
}) {
  const [hover, setHover] = React.useState(null);
  return /*#__PURE__*/React.createElement("div", {
    role: "tablist",
    style: {
      display: "flex",
      gap: "var(--space-6)",
      borderBottom: "1px solid var(--border-default)",
      ...style
    }
  }, items.map(it => {
    const active = it.value === value;
    return /*#__PURE__*/React.createElement("button", {
      key: it.value,
      role: "tab",
      "aria-selected": active,
      onClick: () => onChange && onChange(it.value),
      onMouseEnter: () => setHover(it.value),
      onMouseLeave: () => setHover(null),
      style: {
        position: "relative",
        border: "none",
        background: "transparent",
        padding: "0 0 12px",
        cursor: "pointer",
        fontFamily: "var(--font-heading)",
        fontWeight: "var(--fw-medium)",
        fontSize: "var(--text-base)",
        color: active ? "var(--text-strong)" : hover === it.value ? "var(--text-body)" : "var(--text-muted)",
        transition: "color var(--dur-fast) var(--ease-standard)"
      }
    }, it.label, /*#__PURE__*/React.createElement("span", {
      style: {
        position: "absolute",
        left: 0,
        right: 0,
        bottom: "-1px",
        height: "2px",
        background: active ? "var(--brand-accent)" : "transparent",
        transition: "background var(--dur-fast) var(--ease-standard)"
      }
    }));
  }));
}
Object.assign(__ds_scope, { Tabs });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Tabs.jsx", error: String((e && e.message) || e) }); }

// ui_kits/showroom/Dashboard.jsx
try { (() => {
/* Dashboard — showroom overview. Composes DS Card, Badge, Button, Alert. */
const {
  Card,
  Badge,
  Button,
  Alert
} = window.HeritageDesignSystem_ffe1f3;
function Eyebrow({
  children
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 500,
      fontSize: 12,
      letterSpacing: "var(--tracking-caps)",
      textTransform: "uppercase",
      color: "var(--brand-accent)",
      marginBottom: 8
    }
  }, children);
}
function H1({
  children
}) {
  return /*#__PURE__*/React.createElement("h1", {
    style: {
      margin: 0,
      fontFamily: "var(--font-heading)",
      fontWeight: 500,
      fontSize: "var(--text-3xl)",
      letterSpacing: "var(--tracking-tight)",
      color: "var(--text-strong)"
    }
  }, children);
}
function Stat({
  label,
  value,
  sub,
  tone
}) {
  return /*#__PURE__*/React.createElement(Card, {
    padding: "md"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 500,
      fontSize: 13,
      color: "var(--text-muted)"
    }
  }, label), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 500,
      fontSize: 34,
      letterSpacing: "-0.02em",
      color: "var(--text-strong)",
      margin: "6px 0 4px",
      fontVariantNumeric: "tabular-nums"
    }
  }, value), /*#__PURE__*/React.createElement(Badge, {
    tone: tone
  }, sub));
}
function Dashboard({
  onOpenVehicle
}) {
  const activity = [{
    name: "1968 E-Type Series 1.5",
    meta: "Reserved · £128,000",
    who: "Reserved by A. Fenwick",
    tone: "warning",
    tag: "Reserved"
  }, {
    name: "1991 500SL Roadster",
    meta: "Service complete · 42,110 mi",
    who: "Signed off — R. Doyle",
    tone: "success",
    tag: "Ready"
  }, {
    name: "1973 Carrera RS 2.7",
    meta: "Recall check outstanding",
    who: "Flagged by workshop",
    tone: "danger",
    tag: "Action"
  }, {
    name: "1965 Silver Cloud III",
    meta: "Listed · £96,500",
    who: "Published to showroom",
    tone: "primary",
    tag: "New"
  }];
  return /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1080,
      margin: "0 auto",
      display: "flex",
      flexDirection: "column",
      gap: 24
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "flex-end",
      justifyContent: "space-between",
      gap: 16
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Eyebrow, null, "Tuesday \xB7 9 July"), /*#__PURE__*/React.createElement(H1, null, "Good morning, James")), /*#__PURE__*/React.createElement(Button, {
    variant: "accent",
    iconLeft: /*#__PURE__*/React.createElement(window.Icons.Plus, {
      size: 16
    })
  }, "Add vehicle")), /*#__PURE__*/React.createElement(Alert, {
    tone: "warning",
    title: "Two vehicles need attention",
    onClose: () => {}
  }, "A recall check and an overdue service are outstanding across the collection."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(4, 1fr)",
      gap: 16
    }
  }, /*#__PURE__*/React.createElement(Stat, {
    label: "In collection",
    value: "38",
    sub: "+3 this month",
    tone: "success"
  }), /*#__PURE__*/React.createElement(Stat, {
    label: "Reserved",
    value: "7",
    sub: "2 completing",
    tone: "warning"
  }), /*#__PURE__*/React.createElement(Stat, {
    label: "In workshop",
    value: "5",
    sub: "1 overdue",
    tone: "danger"
  }), /*#__PURE__*/React.createElement(Stat, {
    label: "Enquiries",
    value: "24",
    sub: "This week",
    tone: "primary"
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1.6fr 1fr",
      gap: 16,
      alignItems: "start"
    }
  }, /*#__PURE__*/React.createElement(Card, {
    padding: "md"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      marginBottom: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 500,
      fontSize: 16,
      color: "var(--text-strong)"
    }
  }, "Recent activity"), /*#__PURE__*/React.createElement(Button, {
    variant: "ghost",
    size: "sm",
    iconRight: /*#__PURE__*/React.createElement(window.Icons.ChevronRight, {
      size: 15
    })
  }, "View all")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column"
    }
  }, activity.map((a, i) => /*#__PURE__*/React.createElement("button", {
    key: i,
    onClick: onOpenVehicle,
    style: {
      display: "flex",
      alignItems: "center",
      gap: 14,
      padding: "12px 6px",
      border: "none",
      background: "transparent",
      borderTop: i === 0 ? "none" : "1px solid var(--border-subtle)",
      cursor: "pointer",
      textAlign: "left"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 46,
      height: 34,
      borderRadius: "var(--radius-sm)",
      background: "var(--surface-tint)",
      flexShrink: 0,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      color: "var(--steel-navy)"
    }
  }, /*#__PURE__*/React.createElement(window.Icons.Car, {
    size: 18
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 500,
      fontSize: 14,
      color: "var(--text-strong)"
    }
  }, a.name), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-body)",
      fontWeight: 300,
      fontSize: 13,
      color: "var(--text-muted)"
    }
  }, a.meta)), /*#__PURE__*/React.createElement(Badge, {
    tone: a.tone
  }, a.tag))))), /*#__PURE__*/React.createElement(Card, {
    variant: "inverse",
    padding: "md"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 500,
      fontSize: 16,
      marginBottom: 4
    }
  }, "Concours du Weekend"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-body)",
      fontWeight: 300,
      fontSize: 13,
      color: "rgba(255,255,255,0.72)",
      lineHeight: 1.6,
      marginBottom: 16
    }
  }, "Four vehicles from the collection are entered. Transport departs Friday 06:00."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 10
    }
  }, ["1968 E-Type Series 1.5", "1973 Carrera RS 2.7", "1965 Silver Cloud III", "1957 300SL Gullwing"].map(v => /*#__PURE__*/React.createElement("div", {
    key: v,
    style: {
      display: "flex",
      alignItems: "center",
      gap: 10,
      fontFamily: "var(--font-body)",
      fontWeight: 300,
      fontSize: 13,
      color: "#fff"
    }
  }, /*#__PURE__*/React.createElement(window.Icons.Star, {
    size: 15
  }), v))))));
}
window.Dashboard = Dashboard;
window.KitEyebrow = Eyebrow;
window.KitH1 = H1;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/showroom/Dashboard.jsx", error: String((e && e.message) || e) }); }

// ui_kits/showroom/Icons.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/* Icons — a small inline SVG set (Lucide-style, 1.75 stroke) used across the
   showroom UI kit. Attached to window for the other kit scripts. */
const strokeProps = {
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.75,
  strokeLinecap: "round",
  strokeLinejoin: "round"
};
function Svg({
  children,
  size = 20
}) {
  return /*#__PURE__*/React.createElement("svg", _extends({
    width: size,
    height: size,
    viewBox: "0 0 24 24"
  }, strokeProps), children);
}
const Icons = {
  Gauge: p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
    d: "M12 14l4-4"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M3.5 15a9 9 0 1 1 17 0"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "14",
    r: "1.2",
    fill: "currentColor",
    stroke: "none"
  })),
  Car: p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
    d: "M5 13l1.5-4.5A2 2 0 0 1 8.4 7h7.2a2 2 0 0 1 1.9 1.5L19 13"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M4 13h16v4a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1v-1H7v1a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1z"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "7.5",
    cy: "15.5",
    r: ".6",
    fill: "currentColor",
    stroke: "none"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "16.5",
    cy: "15.5",
    r: ".6",
    fill: "currentColor",
    stroke: "none"
  })),
  Wrench: p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
    d: "M14.7 6.3a4 4 0 0 0-5.2 5.2L4 17l3 3 5.5-5.5a4 4 0 0 0 5.2-5.2l-2.4 2.4-2.1-.5-.5-2.1z"
  })),
  Users: p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("circle", {
    cx: "9",
    cy: "8",
    r: "3"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M3.5 19a5.5 5.5 0 0 1 11 0"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M16 6.5a3 3 0 0 1 0 5.5"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M17 14.2a5.5 5.5 0 0 1 3.5 4.8"
  })),
  Doc: p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
    d: "M6 3h8l4 4v14H6z"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M14 3v4h4"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M9 12h6M9 16h6"
  })),
  Settings: p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "12",
    r: "3"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M12 3v2M12 19v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M3 12h2M19 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"
  })),
  Search: p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("circle", {
    cx: "11",
    cy: "11",
    r: "6"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M20 20l-3.5-3.5"
  })),
  Bell: p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
    d: "M6 9a6 6 0 0 1 12 0c0 5 1.5 6 1.5 6h-15S6 14 6 9z"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M10 19a2 2 0 0 0 4 0"
  })),
  Plus: p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
    d: "M12 5v14M5 12h14"
  })),
  ChevronRight: p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
    d: "M9 6l6 6-6 6"
  })),
  ArrowLeft: p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
    d: "M19 12H5M11 6l-6 6 6 6"
  })),
  Calendar: p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("rect", {
    x: "4",
    y: "5",
    width: "16",
    height: "16",
    rx: "1.5"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M4 9h16M8 3v4M16 3v4"
  })),
  Fuel: p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
    d: "M6 21V5a2 2 0 0 1 2-2h5a2 2 0 0 1 2 2v16"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M4 21h13"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M15 9h2.5a1.5 1.5 0 0 1 1.5 1.5V16a1.5 1.5 0 0 0 3 0V8l-2.5-2.5"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M8 8h5"
  })),
  Road: p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
    d: "M8 21L10 3M16 21L14 3"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M12 6v2M12 11v2M12 16v2"
  })),
  Heart: p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
    d: "M12 20s-7-4.5-7-9.5A3.5 3.5 0 0 1 12 8a3.5 3.5 0 0 1 7 2.5c0 5-7 9.5-7 9.5z"
  })),
  Star: p => /*#__PURE__*/React.createElement(Svg, p, /*#__PURE__*/React.createElement("path", {
    d: "M12 4l2.3 4.7 5.2.8-3.8 3.7.9 5.2L12 16.9 7.4 18.4l.9-5.2L4.5 9.5l5.2-.8z"
  }))
};
window.Icons = Icons;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/showroom/Icons.jsx", error: String((e && e.message) || e) }); }

// ui_kits/showroom/Inventory.jsx
try { (() => {
/* Inventory — the collection grid with filter tabs and vehicle cards.
   Composes DS Tabs, Card, Badge, Tag, Button. */
const {
  Tabs,
  Card,
  Badge,
  Tag,
  Button,
  Input
} = window.HeritageDesignSystem_ffe1f3;
const VEHICLES = [{
  name: "1968 E-Type Series 1.5",
  marque: "Jaguar",
  price: "£128,000",
  miles: "48,900",
  year: 1968,
  status: "reserved",
  accent: "var(--racing-green)"
}, {
  name: "1973 Carrera RS 2.7",
  marque: "Porsche",
  price: "£245,000",
  miles: "61,200",
  year: 1973,
  status: "workshop",
  accent: "var(--orange)"
}, {
  name: "1965 Silver Cloud III",
  marque: "Rolls-Royce",
  price: "£96,500",
  miles: "72,340",
  year: 1965,
  status: "available",
  accent: "var(--oxford-blue)"
}, {
  name: "1957 300SL Gullwing",
  marque: "Mercedes-Benz",
  price: "£1.35m",
  miles: "31,500",
  year: 1957,
  status: "available",
  accent: "var(--steel-navy)"
}, {
  name: "1991 500SL Roadster",
  marque: "Mercedes-Benz",
  price: "£38,000",
  miles: "42,110",
  year: 1991,
  status: "available",
  accent: "var(--muted-purple)"
}, {
  name: "1962 250 GT Lusso",
  marque: "Ferrari",
  price: "£1.1m",
  miles: "24,800",
  year: 1962,
  status: "reserved",
  accent: "var(--dark-red)"
}];
const STATUS = {
  available: {
    tone: "success",
    label: "Available"
  },
  reserved: {
    tone: "warning",
    label: "Reserved"
  },
  workshop: {
    tone: "danger",
    label: "In workshop"
  }
};
function VehicleCard({
  v,
  onOpen
}) {
  return /*#__PURE__*/React.createElement(Card, {
    interactive: true,
    padding: "sm",
    onClick: onOpen,
    style: {
      padding: 0,
      overflow: "hidden",
      display: "flex",
      flexDirection: "column"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: 132,
      background: v.accent,
      position: "relative",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      color: "rgba(255,255,255,0.5)"
    }
  }, /*#__PURE__*/React.createElement(window.Icons.Car, {
    size: 44
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      top: 10,
      left: 10
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: STATUS[v.status].tone,
    solid: v.status === "workshop"
  }, STATUS[v.status].label))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: 16
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 500,
      fontSize: 12,
      letterSpacing: "0.06em",
      textTransform: "uppercase",
      color: "var(--text-subtle)"
    }
  }, v.marque), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 500,
      fontSize: 16,
      color: "var(--text-strong)",
      margin: "4px 0 10px"
    }
  }, v.name), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: 15,
      color: "var(--text-strong)"
    }
  }, v.price), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-body)",
      fontWeight: 300,
      fontSize: 13,
      color: "var(--text-muted)"
    }
  }, v.miles, " mi"))));
}
function Inventory({
  onOpenVehicle
}) {
  const [tab, setTab] = React.useState("all");
  const [filters, setFilters] = React.useState(["1950–1975"]);
  const list = tab === "all" ? VEHICLES : VEHICLES.filter(v => v.status === tab);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1080,
      margin: "0 auto",
      display: "flex",
      flexDirection: "column",
      gap: 20
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "flex-end",
      justifyContent: "space-between",
      gap: 16
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(window.KitEyebrow, null, "38 vehicles"), /*#__PURE__*/React.createElement(window.KitH1, null, "The Collection")), /*#__PURE__*/React.createElement(Button, {
    variant: "accent",
    iconLeft: /*#__PURE__*/React.createElement(window.Icons.Plus, {
      size: 16
    })
  }, "Add vehicle")), /*#__PURE__*/React.createElement(Tabs, {
    value: tab,
    onChange: setTab,
    items: [{
      value: "all",
      label: "All"
    }, {
      value: "available",
      label: "Available"
    }, {
      value: "reserved",
      label: "Reserved"
    }, {
      value: "workshop",
      label: "In workshop"
    }]
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 8,
      flexWrap: "wrap"
    }
  }, filters.map(f => /*#__PURE__*/React.createElement(Tag, {
    key: f,
    onRemove: () => setFilters(filters.filter(x => x !== f))
  }, f)), /*#__PURE__*/React.createElement(Tag, {
    iconLeft: /*#__PURE__*/React.createElement(window.Icons.Plus, {
      size: 13
    })
  }, "Add filter")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(3, 1fr)",
      gap: 16
    }
  }, list.map(v => /*#__PURE__*/React.createElement(VehicleCard, {
    key: v.name,
    v: v,
    onOpen: onOpenVehicle
  }))));
}
window.Inventory = Inventory;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/showroom/Inventory.jsx", error: String((e && e.message) || e) }); }

// ui_kits/showroom/Shell.jsx
try { (() => {
/* Shell — top bar + left navigation rail for the showroom app.
   Composes DS Badge, IconButton, Input, Tooltip. */
const {
  Badge,
  IconButton,
  Input,
  Tooltip
} = window.HeritageDesignSystem_ffe1f3;
function NavItem({
  icon: Icon,
  label,
  active,
  onClick
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("button", {
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      display: "flex",
      alignItems: "center",
      gap: 12,
      width: "100%",
      padding: "10px 14px",
      border: "none",
      cursor: "pointer",
      textAlign: "left",
      borderRadius: "var(--radius-sm)",
      fontFamily: "var(--font-heading)",
      fontWeight: "var(--fw-medium)",
      fontSize: 14,
      color: active ? "#fff" : hover ? "#fff" : "rgba(255,255,255,0.66)",
      background: active ? "rgba(255,255,255,0.12)" : hover ? "rgba(255,255,255,0.06)" : "transparent",
      borderLeft: "2px solid " + (active ? "var(--brand-accent)" : "transparent"),
      transition: "background var(--dur-fast) var(--ease-standard), color var(--dur-fast) var(--ease-standard)"
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    size: 18
  }), label);
}
function Shell({
  view,
  setView,
  children
}) {
  const nav = [{
    id: "dashboard",
    label: "Overview",
    icon: window.Icons.Gauge
  }, {
    id: "inventory",
    label: "Collection",
    icon: window.Icons.Car
  }, {
    id: "service",
    label: "Service",
    icon: window.Icons.Wrench
  }, {
    id: "clients",
    label: "Clients",
    icon: window.Icons.Users
  }, {
    id: "documents",
    label: "Documents",
    icon: window.Icons.Doc
  }];
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      height: "100vh",
      background: "var(--surface-page)",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("aside", {
    style: {
      width: 236,
      flexShrink: 0,
      background: "var(--oxford-blue)",
      display: "flex",
      flexDirection: "column",
      padding: "20px 14px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 12,
      padding: "4px 8px 20px",
      fontFamily: "var(--font-heading)",
      fontWeight: "var(--fw-medium)",
      color: "#fff",
      letterSpacing: "var(--tracking-caps)",
      textTransform: "uppercase",
      fontSize: 15
    }
  }, "Heritage", /*#__PURE__*/React.createElement("span", {
    style: {
      width: 2,
      height: 18,
      background: "var(--brand-accent)"
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontWeight: "var(--fw-light)",
      color: "var(--antique-gold)",
      textTransform: "none",
      letterSpacing: 0
    }
  }, "Motoring")), /*#__PURE__*/React.createElement("nav", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 3
    }
  }, nav.map(n => /*#__PURE__*/React.createElement(NavItem, {
    key: n.id,
    icon: n.icon,
    label: n.label,
    active: view === n.id,
    onClick: () => setView(n.id)
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: "auto",
      display: "flex",
      flexDirection: "column",
      gap: 3
    }
  }, /*#__PURE__*/React.createElement(NavItem, {
    icon: window.Icons.Settings,
    label: "Settings",
    active: false,
    onClick: () => {}
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 10,
      padding: "12px 8px 2px",
      marginTop: 8,
      borderTop: "1px solid rgba(255,255,255,0.12)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 32,
      height: 32,
      borderRadius: "50%",
      background: "var(--leather-brown)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      color: "#fff",
      fontFamily: "var(--font-heading)",
      fontWeight: 500,
      fontSize: 13
    }
  }, "JM"), /*#__PURE__*/React.createElement("div", {
    style: {
      lineHeight: 1.2
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      color: "#fff",
      fontFamily: "var(--font-heading)",
      fontWeight: 500,
      fontSize: 13
    }
  }, "J. Mercer"), /*#__PURE__*/React.createElement("div", {
    style: {
      color: "rgba(255,255,255,0.5)",
      fontFamily: "var(--font-body)",
      fontWeight: 300,
      fontSize: 12
    }
  }, "Sales"))))), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      display: "flex",
      flexDirection: "column",
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("header", {
    style: {
      height: 64,
      flexShrink: 0,
      display: "flex",
      alignItems: "center",
      gap: 16,
      padding: "0 28px",
      background: "var(--surface-card)",
      borderBottom: "1px solid var(--border-default)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 320,
      maxWidth: "40%"
    }
  }, /*#__PURE__*/React.createElement(Input, {
    size: "sm",
    placeholder: "Search VIN, model or client\u2026",
    iconLeft: /*#__PURE__*/React.createElement(window.Icons.Search, {
      size: 16
    })
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      marginLeft: "auto",
      display: "flex",
      alignItems: "center",
      gap: 8
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: "gold"
  }, "Concours Season"), /*#__PURE__*/React.createElement(Tooltip, {
    label: "Notifications"
  }, /*#__PURE__*/React.createElement(IconButton, {
    label: "Notifications",
    variant: "ghost"
  }, /*#__PURE__*/React.createElement(window.Icons.Bell, {
    size: 19
  }))))), /*#__PURE__*/React.createElement("main", {
    style: {
      flex: 1,
      overflow: "auto",
      padding: 28
    }
  }, children)));
}
window.Shell = Shell;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/showroom/Shell.jsx", error: String((e && e.message) || e) }); }

// ui_kits/showroom/VehicleDetail.jsx
try { (() => {
/* VehicleDetail — a single vehicle record with tabs, spec grid, gallery,
   and actions. Composes DS Tabs, Card, Badge, Button, Alert. */
const {
  Tabs,
  Card,
  Badge,
  Button,
  Alert
} = window.HeritageDesignSystem_ffe1f3;
function SpecRow({
  icon: Icon,
  label,
  value
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 12,
      padding: "12px 0",
      borderTop: "1px solid var(--border-subtle)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: "var(--steel-navy)"
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    size: 18
  })), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      fontFamily: "var(--font-body)",
      fontWeight: 300,
      fontSize: 14,
      color: "var(--text-muted)"
    }
  }, label), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 500,
      fontSize: 14,
      color: "var(--text-strong)"
    }
  }, value));
}
function VehicleDetail({
  onBack
}) {
  const [tab, setTab] = React.useState("spec");
  const thumbs = ["var(--racing-green)", "var(--steel-navy)", "var(--leather-brown)", "var(--grey-dark)"];
  const [active, setActive] = React.useState(0);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1080,
      margin: "0 auto",
      display: "flex",
      flexDirection: "column",
      gap: 20
    }
  }, /*#__PURE__*/React.createElement("button", {
    onClick: onBack,
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: 8,
      border: "none",
      background: "transparent",
      cursor: "pointer",
      fontFamily: "var(--font-heading)",
      fontWeight: 500,
      fontSize: 14,
      color: "var(--text-muted)",
      padding: 0
    }
  }, /*#__PURE__*/React.createElement(window.Icons.ArrowLeft, {
    size: 17
  }), " Back to collection"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1.4fr 1fr",
      gap: 28,
      alignItems: "start"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 12
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: 340,
      borderRadius: "var(--radius-lg)",
      background: thumbs[active],
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      color: "rgba(255,255,255,0.45)",
      border: "1px solid var(--border-subtle)"
    }
  }, /*#__PURE__*/React.createElement(window.Icons.Car, {
    size: 80
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(4,1fr)",
      gap: 12
    }
  }, thumbs.map((c, i) => /*#__PURE__*/React.createElement("button", {
    key: i,
    onClick: () => setActive(i),
    style: {
      height: 68,
      borderRadius: "var(--radius-sm)",
      background: c,
      border: "2px solid " + (i === active ? "var(--brand-accent)" : "transparent"),
      cursor: "pointer"
    }
  })))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 8,
      marginBottom: 8
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: "warning",
    dot: true
  }, "Reserved"), /*#__PURE__*/React.createElement(Badge, {
    tone: "gold"
  }, "Matching numbers")), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 500,
      fontSize: 12,
      letterSpacing: "0.06em",
      textTransform: "uppercase",
      color: "var(--text-subtle)"
    }
  }, "Jaguar"), /*#__PURE__*/React.createElement("h1", {
    style: {
      margin: "4px 0 8px",
      fontFamily: "var(--font-heading)",
      fontWeight: 500,
      fontSize: "var(--text-2xl)",
      letterSpacing: "-0.02em",
      color: "var(--text-strong)"
    }
  }, "1968 E-Type Series 1.5"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: 22,
      color: "var(--text-strong)",
      marginBottom: 16
    }
  }, "\xA3128,000"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 10,
      marginBottom: 20
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    fullWidth: true
  }, "Arrange viewing"), /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    iconLeft: /*#__PURE__*/React.createElement(window.Icons.Heart, {
      size: 16
    })
  }, "Save")), /*#__PURE__*/React.createElement(Card, {
    variant: "sunken",
    padding: "sm"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "0 4px"
    }
  }, /*#__PURE__*/React.createElement(SpecRow, {
    icon: window.Icons.Calendar,
    label: "Year",
    value: "1968"
  }), /*#__PURE__*/React.createElement(SpecRow, {
    icon: window.Icons.Road,
    label: "Odometer",
    value: "48,900 mi"
  }), /*#__PURE__*/React.createElement(SpecRow, {
    icon: window.Icons.Fuel,
    label: "Engine",
    value: "4.2L Straight-6"
  }), /*#__PURE__*/React.createElement(SpecRow, {
    icon: window.Icons.Doc,
    label: "VIN",
    value: "1E15473"
  }))))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 4
    }
  }, /*#__PURE__*/React.createElement(Tabs, {
    value: tab,
    onChange: setTab,
    items: [{
      value: "spec",
      label: "Specification"
    }, {
      value: "history",
      label: "Service history"
    }, {
      value: "provenance",
      label: "Provenance"
    }]
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      paddingTop: 20
    }
  }, tab === "spec" && /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(3,1fr)",
      gap: 24
    }
  }, [["Transmission", "4-speed manual"], ["Drive", "Rear-wheel drive"], ["Colour", "British Racing Green"], ["Interior", "Biscuit leather"], ["Power", "265 bhp"], ["0–60", "6.8 s"]].map(([k, v]) => /*#__PURE__*/React.createElement("div", {
    key: k
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-body)",
      fontWeight: 300,
      fontSize: 13,
      color: "var(--text-muted)"
    }
  }, k), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 500,
      fontSize: 15,
      color: "var(--text-strong)",
      marginTop: 3
    }
  }, v)))), tab === "history" && /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 12
    }
  }, /*#__PURE__*/React.createElement(Alert, {
    tone: "success",
    title: "Full service history"
  }, "Continuous records from 1972, last serviced 2,400 miles ago."), [["June 2024", "Major service · marque specialist"], ["Aug 2021", "Brake overhaul, new hoses"], ["Mar 2019", "Concours restoration completed"]].map(([d, t]) => /*#__PURE__*/React.createElement("div", {
    key: d,
    style: {
      display: "flex",
      gap: 16,
      padding: "10px 2px",
      borderTop: "1px solid var(--border-subtle)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 96,
      flexShrink: 0,
      fontFamily: "var(--font-mono)",
      fontSize: 13,
      color: "var(--text-muted)"
    }
  }, d), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-body)",
      fontWeight: 300,
      fontSize: 14,
      color: "var(--text-body)"
    }
  }, t)))), tab === "provenance" && /*#__PURE__*/React.createElement("p", {
    style: {
      maxWidth: 640,
      fontFamily: "var(--font-body)",
      fontWeight: 300,
      fontSize: 15,
      lineHeight: 1.65,
      color: "var(--text-body)",
      margin: 0
    }
  }, "Three owners from new. Supplied by the London distributor in 1968, retained in a single private collection for 31 years, and restored to concours standard in 2019. Accompanied by original buff logbook, tool roll and continuous invoices."))));
}
window.VehicleDetail = VehicleDetail;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/showroom/VehicleDetail.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.IconButton = __ds_scope.IconButton;

__ds_ns.Tag = __ds_scope.Tag;

__ds_ns.Alert = __ds_scope.Alert;

__ds_ns.Dialog = __ds_scope.Dialog;

__ds_ns.Tooltip = __ds_scope.Tooltip;

__ds_ns.Checkbox = __ds_scope.Checkbox;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Radio = __ds_scope.Radio;

__ds_ns.Select = __ds_scope.Select;

__ds_ns.Switch = __ds_scope.Switch;

__ds_ns.Tabs = __ds_scope.Tabs;

})();
