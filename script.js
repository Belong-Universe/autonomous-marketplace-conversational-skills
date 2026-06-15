const copyButtons = document.querySelectorAll("[data-copy-target]");

copyButtons.forEach((button) => {
  button.addEventListener("click", async () => {
    const target = document.getElementById(button.dataset.copyTarget);
    if (!target) return;

    const originalLabel = button.textContent;
    try {
      await navigator.clipboard.writeText(target.textContent.trim());
      button.textContent = "Copied";
      window.setTimeout(() => {
        button.textContent = originalLabel;
      }, 1400);
    } catch {
      button.textContent = "Select";
      target.closest("pre")?.focus();
    }
  });
});

const tabs = document.querySelector("[data-tabs]");

if (tabs) {
  const tabButtons = tabs.querySelectorAll("[role='tab']");
  const panels = tabs.querySelectorAll("[role='tabpanel']");

  tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const panelId = `tab-${button.dataset.tab}`;

      tabButtons.forEach((candidate) => {
        candidate.setAttribute("aria-selected", String(candidate === button));
      });

      panels.forEach((panel) => {
        const isActive = panel.id === panelId;
        panel.hidden = !isActive;
        panel.classList.toggle("active", isActive);
      });
    });
  });
}
