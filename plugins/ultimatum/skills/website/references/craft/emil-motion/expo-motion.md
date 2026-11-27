# Expo and React Native motion: the rules

Read when an Expo or React Native app needs motion: which tool to reach for, what may animate, how to keep frames off the JavaScript thread, press and haptic feedback, reduced motion, and screen and sheet transitions. The recipes are in `expo-recipes.md`. The gate (`gate.md`), curves (`easing-and-duration.md`) and springs (`springs.md`) still decide whether and how long; this file maps them onto native tools.

Code here was type-checked with TypeScript 5.9 in strict mode against react-native 0.81, react-native-reanimated 4.8, react-native-worklets 0.14, react-native-gesture-handler 2.33, expo-haptics 58, react-native-keyboard-controller 1.24 and @react-navigation/native-stack 7.21. It has not been run on a phone or simulator; check it on a device before you call it done.

## Pick the lightest tool that does the job

Go down the list and stop at the first one that fits.

1. **Native navigation.** A pushed screen, a modal, a sheet with detents, a large title that shrinks on scroll, native tabs, a context menu with preview, pull to refresh: let the platform do it (native-stack, Expo Router `Stack`, `formSheet`). It matches the OS, respects the user's settings and costs no code.
2. **Layout animations.** Something appears, leaves, or moves because the list changed: Reanimated `entering`, `exiting` and `layout` props (`FadeInDown`, `FadeOut`, `LinearTransition`).
3. **A shared value and an animated style.** A state change the user caused (pressed, open, selected): `useSharedValue` plus `withTiming` or `withSpring` inside `useAnimatedStyle`.
4. **A gesture driving a shared value.** The finger owns the motion (drag, swipe, pinch): Gesture Handler's `Gesture.Pan()` writing to a shared value, with a spring that takes the release velocity.
5. **Scroll or keyboard driving a shared value.** `useAnimatedScrollHandler`, `useAnimatedKeyboard` or keyboard-controller's sticky views.
6. **Lottie** for an illustration a designer made; never for UI that should react to touch.
7. **A canvas library** (Skia) only for hundreds of moving shapes or custom drawing. Everything else stays in views.

## What may animate

Same rule as the web (`performance.md`): `transform` (translate, scale, rotate) and `opacity` are cheap and run on the UI thread. Width, height, padding, margin, `top` and `left` re-run layout every frame; on a list row that is a dropped frame. To make a header shorter, move it up with `translateY` and keep its height fixed (`expo-recipes.md`, collapsing header). Colour is fine through `interpolateColor`. Shadows and blur views are expensive on Android; fade a pre-drawn shadow instead.

## Keep frames off the JavaScript thread

- Animated style callbacks, gesture callbacks and scroll handlers are **worklets**: they run on the UI thread and must only touch shared values and other worklets. A helper they call needs the `'worklet'` directive (the rubber-band function in `expo-recipes.md`).
- To call ordinary JS (set React state, navigate, fire a haptic) from a worklet, hop with `scheduleOnRN(fn, ...args)` from react-native-worklets (`runOnJS` is the older name). Never call `setState` straight from a gesture.
- Don't read `sharedValue.value` during render; it is a snapshot and causes confusion. Read it inside worklets.
- Don't store a whole object in a shared value and mutate one field; assign a new value or use one shared value per number.
- React re-renders don't drive animation. If a parent re-renders 60 times a second, the bug is upstream of the animation.

## Timing or spring

| The motion is | Use | Numbers |
|---|---|---|
| A reply to a tap (press, toggle, select) | `withTiming` going in, `withSpring` coming back | in 80–120 ms; back with `duration` 250–300 ms and `dampingRatio` 0.7–0.8 |
| Released by a finger | `withSpring` with `velocity` from the gesture | `dampingRatio` 0.8–0.9 so it lands without bouncing past |
| Opening or moving a panel | `withSpring` with `duration` and `dampingRatio` | 300–400 ms, 0.85 |
| A fade or colour change | `withTiming` | 150–250 ms, ease-out |
| A loop (spinner, skeleton) | `withRepeat(withTiming(...), -1)` | stop it when the content arrives |

Reanimated 4 springs accept `duration` plus `dampingRatio` (easy to reason about) or `mass`, `stiffness` and `damping` (physics). Pick one style per app.

## Press, not hover

Phones have no hover, so the press state carries all the feedback a hover would on the web. Every tappable thing:

- reacts on **press in**, not on release: scale to 0.96–0.98 or dim to 0.85–0.9 within about 100 ms;
- comes back with a short spring on **press out**, whether or not the tap counted;
- has a hit area of at least 44 × 44 pt on iOS and 48 × 48 dp on Android (`hitSlop` grows it without growing the drawing);
- sets `accessibilityRole` and, for toggles, `accessibilityState`.

```tsx
import { Pressable, Text } from 'react-native';
import Animated, { useAnimatedStyle, useSharedValue, withSpring, withTiming } from 'react-native-reanimated';
import * as Haptics from 'expo-haptics';

const AnimatedPressable = Animated.createAnimatedComponent(Pressable);

export function PressButton({ label, onPress }: { label: string; onPress: () => void }) {
  const pressed = useSharedValue(0);
  const style = useAnimatedStyle(() => ({
    transform: [{ scale: 1 - pressed.value * 0.04 }],
    opacity: 1 - pressed.value * 0.1,
  }));
  return (
    <AnimatedPressable
      accessibilityRole="button"
      onPressIn={() => { pressed.value = withTiming(1, { duration: 90 }); }}
      onPressOut={() => { pressed.value = withSpring(0, { duration: 280, dampingRatio: 0.7 }); }}
      onPress={() => { Haptics.selectionAsync(); onPress(); }}
      hitSlop={8}
      style={[{ minHeight: 48, paddingHorizontal: 20, justifyContent: 'center', borderRadius: 12 }, style]}>
      <Text>{label}</Text>
    </AnimatedPressable>
  );
}
```

## Haptics

Haptics confirm; they don't decorate. One light tap for a selection change or a snap point (`Haptics.selectionAsync`), a success or error notification when a task finishes (`notificationAsync`), and a light or medium impact when a drag crosses a line (`impactAsync`). Never on every scroll frame, never on plain navigation, and never more than one per gesture moment. They are skipped silently on devices without a motor, so never put meaning only in a haptic. The fire-once pattern is the last recipe in `expo-recipes.md`.

## Reduced motion

Read the setting with `useReducedMotion()` (a plain boolean, safe in render), and pass `reduceMotion: ReduceMotion.System` to animation configs and layout animations so Reanimated follows the OS. With motion reduced, movement becomes instant or a short fade; opacity and colour may stay. Gestures still track the finger, because the user is moving it themselves. Loops stop.

```tsx
import { ReduceMotion, useReducedMotion, withSpring, withTiming } from 'react-native-reanimated';

export function useMotion() {
  const reduce = useReducedMotion();
  return {
    reduce,
    // Position changes become instant; fades stay but shorten.
    move: (to: number) => {
      'worklet';
      return withSpring(to, { duration: 300, dampingRatio: 0.85, reduceMotion: ReduceMotion.System });
    },
    fade: (to: number) => {
      'worklet';
      return withTiming(to, { duration: reduce ? 120 : 200 });
    },
  };
}
```

## Screens and sheets

Use the native stack and set the transition per screen; don't rebuild a push or a sheet in JS.

```tsx
import type { NativeStackNavigationOptions } from '@react-navigation/native-stack';

// Expo Router: <Stack.Screen name="..." options={...} /> takes these native-stack options.
export const push: NativeStackNavigationOptions = { animation: 'slide_from_right' }; // the platform default; leave it
export const detailFade: NativeStackNavigationOptions = { animation: 'fade', animationDuration: 200 };
export const sheet: NativeStackNavigationOptions = {
  presentation: 'formSheet',
  sheetAllowedDetents: [0.5, 1],
  sheetGrabberVisible: true,
  sheetCornerRadius: 20,
};
export const modal: NativeStackNavigationOptions = { presentation: 'modal' };
```

- Keep the platform default for ordinary pushes. A fade suits a detail that opens from the same place; a sheet suits a short task the user will dismiss; a full modal suits a flow with its own steps.
- A `formSheet` with detents gives the native grabber, drag and dismiss for free. Build your own sheet (`expo-recipes.md`) only when it must sit over a screen without being a route.
- Shared-element transitions between screens are still experimental in Reanimated; don't ship one without testing both platforms.

## 120 fps screens

ProMotion iPhones and many Android phones refresh at 120 Hz. Reanimated runs at the display's rate when work stays on the UI thread. On iOS, add `CADisableMinimumFrameDurationOnPhone` set to true in `Info.plist` (Expo: `ios.infoPlist` in app config) or core animation caps your app at 60. Test motion in a release build: the dev build and its debugger are slow on purpose.

## Check before you call it done

- Release build on a real device, both platforms if you ship both.
- Turn on Reduce Motion (iOS Settings, Accessibility, Motion; Android, Remove animations) and walk the screens.
- Press every control: does it react before the finger lifts?
- Drag every sheet and row slowly, then flick it: slow should snap back, a flick should finish.
- Watch the performance monitor (shake menu, Perf Monitor): the UI thread should hold the display rate while you scroll and drag.
