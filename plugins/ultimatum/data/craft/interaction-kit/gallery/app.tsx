import * as React from "react";
import { createRoot } from "react-dom/client";
import { PressButton } from "../components/press-button";
import { CopyButton } from "../components/copy-button";
import { HoldToConfirm } from "../components/hold-to-confirm";
import { Magnetic } from "../components/magnetic";
import { SegmentedControl } from "../components/segmented-control";
import { Tabs } from "../components/tabs";
import { NumberTicker } from "../components/number-ticker";
import { TextReveal } from "../components/text-reveal";
import { Accordion } from "../components/accordion";
import { ToastProvider, useToast } from "../components/toast";
import { Drawer } from "../components/drawer";
import { TiltCard } from "../components/tilt-card";
import { SpotlightCard } from "../components/spotlight-card";
import { Marquee } from "../components/marquee";
import { ScrambleText } from "../components/scramble-text";
import { BorderBeam, ShimmerText } from "../components/border-beam";
import { FloatingInput } from "../components/floating-input";
import { OtpInput } from "../components/otp-input";
import { TagInput } from "../components/tag-input";
import { CommandPalette } from "../components/command-palette";
import { Dock } from "../components/dock";
import { Stepper } from "../components/stepper";
import { ExpandableCards } from "../components/expandable-card";
import { ThemeToggle } from "../components/theme-toggle";
import { Rating, QuickFeedback } from "../components/rating";
import { ReorderList, type ReorderItem } from "../components/reorder-list";
import { Carousel } from "../components/carousel";
import { SwipeDeck } from "../components/swipe-deck";
import { MorphPopover } from "../components/morph-popover";
import { SplitButton } from "../components/split-button";
import { ScrubNumber } from "../components/scrub-number";

const Dot = () => <svg viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="8" /></svg>;
function Sec({ t, children }: { t: string; children: React.ReactNode }) {
  return <section className="flex flex-col gap-3 rounded-[var(--radius)] border border-border p-4"><h2 className="m-0 text-sm font-semibold text-muted-foreground">{t}</h2>{children}</section>;
}
function ToastDemo() { const toast = useToast(); return <PressButton onClick={() => toast({ title: "Saved", body: "Your changes are live.", tone: "success" })}>Show toast</PressButton>; }

function App() {
  const [st, setSt] = React.useState<"idle" | "busy" | "done" | "failed">("idle");
  const [seg, setSeg] = React.useState<"day" | "week" | "month">("week");
  const [drawer, setDrawer] = React.useState(false);
  const [otp, setOtp] = React.useState("12");
  const [tags, setTags] = React.useState(["react", "motion"]);
  const [cmd, setCmd] = React.useState(false);
  const [theme, setTheme] = React.useState<"light" | "dark">("light");
  const [stars, setStars] = React.useState(3);
  const [list, setList] = React.useState<ReorderItem[]>([{ id: "a", label: "Design" }, { id: "b", label: "Build" }, { id: "c", label: "Ship" }]);
  const [num, setNum] = React.useState(16);
  React.useEffect(() => { document.documentElement.classList.toggle("dark", theme === "dark"); }, [theme]);
  return (
    <ToastProvider>
      <main className="mx-auto grid max-w-5xl gap-4 p-4 sm:grid-cols-2">
        <h1 className="sr-only">Interaction kit gallery</h1>
        <Sec t="PressButton"><div className="flex gap-2"><PressButton state={st} onClick={() => { setSt("busy"); setTimeout(() => setSt("done"), 600); }}>Save</PressButton><PressButton variant="outline">Cancel</PressButton></div></Sec>
        <Sec t="CopyButton"><CopyButton value="npm i motion" /></Sec>
        <Sec t="HoldToConfirm"><HoldToConfirm onConfirm={() => {}}>Hold to delete</HoldToConfirm></Sec>
        <Sec t="Magnetic"><Magnetic><PressButton>Hover me</PressButton></Magnetic></Sec>
        <Sec t="SegmentedControl"><SegmentedControl label="Range" value={seg} onChange={setSeg} options={[{ value: "day", label: "Day" }, { value: "week", label: "Week" }, { value: "month", label: "Month" }]} /></Sec>
        <Sec t="Tabs"><Tabs label="Settings" tabs={[{ id: "a", label: "Account", panel: <p className="m-0 text-sm">Account panel</p> }, { id: "b", label: "Billing", panel: <p className="m-0 text-sm">Billing panel</p> }]} /></Sec>
        <Sec t="NumberTicker"><p className="m-0 text-3xl font-semibold"><NumberTicker value={12840} format={{ style: "currency", currency: "USD", maximumFractionDigits: 0 }} /></p></Sec>
        <Sec t="TextReveal"><TextReveal text="Interfaces that feel alive" className="m-0 text-2xl font-semibold" /></Sec>
        <Sec t="Accordion"><Accordion items={[{ id: "1", title: "What is it?", body: "A kit." }, { id: "2", title: "Licence?", body: "Ours." }]} /></Sec>
        <Sec t="Toast"><ToastDemo /></Sec>
        <Sec t="Drawer"><PressButton onClick={() => setDrawer(true)}>Open drawer</PressButton><Drawer open={drawer} onClose={() => setDrawer(false)} title="Filters"><p className="text-sm">Content</p></Drawer></Sec>
        <Sec t="TiltCard"><TiltCard className="p-6"><p className="m-0">Tilt</p></TiltCard></Sec>
        <Sec t="SpotlightCard"><SpotlightCard className="p-6"><p className="m-0">Spotlight</p></SpotlightCard></Sec>
        <Sec t="Marquee"><Marquee label="Customers"><span>Alpha</span><span>Beta</span><span>Gamma</span><span>Delta</span></Marquee></Sec>
        <Sec t="ScrambleText"><ScrambleText text="SYSTEM READY" /></Sec>
        <Sec t="BorderBeam / Shimmer"><BorderBeam><p className="m-0 p-4">Beam <ShimmerText>New</ShimmerText></p></BorderBeam></Sec>
        <Sec t="FloatingInput"><FloatingInput label="Email" type="email" hint="We never share it." /></Sec>
        <Sec t="OtpInput"><OtpInput value={otp} onChange={setOtp} /></Sec>
        <Sec t="TagInput"><TagInput label="Topics" value={tags} onChange={setTags} /></Sec>
        <Sec t="CommandPalette"><PressButton onClick={() => setCmd(true)}>Open command menu</PressButton><CommandPalette open={cmd} onOpenChange={setCmd} commands={[{ id: "n", label: "New file", group: "File", hint: "N", run: () => {} }, { id: "t", label: "Toggle theme", group: "View", run: () => setTheme((t) => t === "dark" ? "light" : "dark") }]} /></Sec>
        <Sec t="Dock"><Dock items={[{ id: "h", label: "Home", icon: <Dot /> }, { id: "s", label: "Search", icon: <Dot /> }, { id: "m", label: "Mail", icon: <Dot />, href: "#mail" }]} /></Sec>
        <Sec t="Stepper"><Stepper steps={["Cart", "Details", "Pay"]} current={1} /></Sec>
        <Sec t="ThemeToggle"><ThemeToggle theme={theme} onToggle={() => setTheme((t) => t === "dark" ? "light" : "dark")} /></Sec>
        <Sec t="Rating / QuickFeedback"><Rating label="Rate this" value={stars} onChange={setStars} /><QuickFeedback onSubmit={() => {}} /></Sec>
        <Sec t="ReorderList"><ReorderList label="Steps" items={list} onReorder={setList} /></Sec>
        <Sec t="Carousel"><Carousel label="Photos" slides={[1, 2, 3, 4].map((n) => <div key={n} className="grid aspect-video place-items-center rounded-[var(--radius)] bg-muted">Slide {n}</div>)} /></Sec>
        <Sec t="SwipeDeck"><div className="w-56"><SwipeDeck onDecide={() => {}} cards={[1, 2, 3].map((n) => ({ id: String(n), label: "Card " + n, content: <p className="m-0 p-6">Card {n}</p> }))} /></div></Sec>
        <Sec t="MorphPopover"><MorphPopover label="Feedback">{(close) => <div className="flex flex-col gap-2"><label htmlFor="mp" className="text-sm">Your note</label><textarea id="mp" className="rounded-[var(--radius)] border border-input bg-background p-2 text-sm" /><PressButton onClick={close}>Send</PressButton></div>}</MorphPopover></Sec>
        <Sec t="SplitButton"><SplitButton primary={{ id: "s", label: "Save", run: () => {} }} more={[{ id: "d", label: "Save as draft", run: () => {} }, { id: "t", label: "Save as template", run: () => {} }]} moreLabel="More save options" /></Sec>
        <Sec t="ScrubNumber"><ScrubNumber label="Size" value={num} onChange={setNum} min={0} max={96} unit="px" /></Sec>
        <Sec t="ExpandableCards"><ExpandableCards items={[{ id: "x", title: "Project X", subtitle: "Case study", body: "Long story." }, { id: "y", title: "Project Y", body: "Another." }]} /></Sec>
      </main>
    </ToastProvider>
  );
}
createRoot(document.getElementById("root")!).render(<App />);
