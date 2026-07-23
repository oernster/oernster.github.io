/* Obscured contact bootstrap for ernster.dev, mirroring crankthecode.com's
   technique so both sites share one contact address and one bot-resistance
   approach. The address never appears in the served HTML or in this file. */
window.ED_CONTACT = (function () {
  // Encoded source-of-truth pieces.
  // These values are safe to expose because they do not match email patterns.
  const decode = (v) => {
    try {
      return atob(v);
    } catch (e) {
      return "";
    }
  };

  const user = decode("b2VybnN0ZXI=");
  const domain = decode("Y29kZWNyYWZ0ZXI=");
  const tld = decode("dWs=");

  const address = user + "@" + domain + "." + tld;
  const link = "mai" + "lto:" + address;

  return { user, domain, tld, address, link };
})();

// Click-to-reveal: avoid rendering the email address into static HTML.
// First activation both reveals and navigates to mailto.
(function () {
  function attachEmailReveal(el) {
    if (!el) {
      return;
    }

    function openEmail(e) {
      // Prevent following the no-JS fallback href.
      if (e && typeof e.preventDefault === "function") {
        e.preventDefault();
      }

      const c = window.ED_CONTACT;
      if (!c) {
        return;
      }

      // Keep the visible label; only the href gains the address.
      el.setAttribute("href", c.link);

      // Remove handlers so the next activation behaves as a normal anchor.
      el.removeEventListener("click", openEmail);
      el.removeEventListener("keydown", onKeydown);

      // Open the mail client immediately on the same activation.
      window.location.href = c.link;
    }

    function onKeydown(e) {
      const key = e && e.key;
      if (key === "Enter" || key === " ") {
        openEmail(e);
      }
    }

    el.addEventListener("click", openEmail);
    el.addEventListener("keydown", onKeydown);
  }

  window.addEventListener("DOMContentLoaded", function () {
    const nodes = document.querySelectorAll("[data-email-reveal]");
    nodes.forEach((el) => attachEmailReveal(el));
  });
})();
