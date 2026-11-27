# Expo and React Native motion: recipes

Read when you are building one of these in an Expo or React Native app: a drag-to-close sheet, a swipe-to-delete row, a collapsing header, list entrances, a composer that rides the keyboard, a sliding tab indicator, a toast, or a haptic that fires once at a threshold. The rules behind them (which tool, what may animate, the UI thread, reduced motion) are in `expo-motion.md`; the press button, screen options and reduced-motion hook are there too.

Every recipe is our own code and was type-checked in strict mode against the versions listed in `expo-motion.md`; none has been run on a device yet. Each assumes the app root has `GestureHandlerRootView` (and `KeyboardProvider` for the keyboard recipe).

## Drag-to-close sheet

Down follows the finger exactly; up resists, so the sheet can't be pulled off the top. On release it closes if it has travelled a quarter of the screen or was flicked fast, carrying the finger's speed into the spring; otherwise it springs home. The close callback runs only when the spring finishes.

```tsx
import { ReactNode } from 'react';
import { useWindowDimensions } from 'react-native';
import { GestureDetector, Gesture } from 'react-native-gesture-handler';
import Animated, { useAnimatedStyle, useSharedValue, withSpring } from 'react-native-reanimated';
import { scheduleOnRN } from 'react-native-worklets';

const band = (d: number, size: number) => {
  'worklet';
  return (1 - 1 / ((d * 0.55) / size + 1)) * size;
};

export function DragSheet({ children, onClose }: { children: ReactNode; onClose: () => void }) {
  const { height } = useWindowDimensions();
  const y = useSharedValue(0);
  const pan = Gesture.Pan()
    .onChange((e) => {
      // down follows the finger 1:1, up resists
      y.value = e.translationY > 0 ? e.translationY : -band(-e.translationY, height);
    })
    .onEnd((e) => {
      const close = y.value > height * 0.25 || e.velocityY > 900;
      if (close) {
        y.value = withSpring(height, { velocity: e.velocityY, overshootClamping: true }, (done) => {
          if (done) scheduleOnRN(onClose);
        });
      } else {
        y.value = withSpring(0, { velocity: e.velocityY, dampingRatio: 0.85 });
      }
    });
  const style = useAnimatedStyle(() => ({ transform: [{ translateY: y.value }] }));
  return (
    <GestureDetector gesture={pan}>
      <Animated.View accessibilityViewIsModal style={[{ position: 'absolute', left: 0, right: 0, bottom: 0 }, style]}>
        {children}
      </Animated.View>
    </GestureDetector>
  );
}
```

Check: slow drag a short way and let go (it returns); flick (it closes even from a short distance); pull up (it gives a little and comes back). Add a visible close button: a drag is never the only way out.

## Swipe-to-delete row

The pan only takes over once the finger has clearly gone sideways, so the list still scrolls. Half-open snaps to show the delete button; a long or fast swipe deletes. After delete, the row fades out and the rows below close the gap with a layout transition.

```tsx
import { ReactNode } from 'react';
import { GestureDetector, Gesture } from 'react-native-gesture-handler';
import Animated, { useAnimatedStyle, useSharedValue, withTiming, withSpring, FadeOut, LinearTransition } from 'react-native-reanimated';
import { scheduleOnRN } from 'react-native-worklets';

const REVEAL = 88; // width of the delete button behind the row

export function SwipeRow({ children, onDelete }: { children: ReactNode; onDelete: () => void }) {
  const x = useSharedValue(0);
  const start = useSharedValue(0);
  const pan = Gesture.Pan()
    .activeOffsetX([-12, 12]) // let vertical scroll win until the finger clearly goes sideways
    .failOffsetY([-10, 10])
    .onStart(() => { start.value = x.value; })
    .onChange((e) => { x.value = Math.min(0, start.value + e.translationX); })
    .onEnd((e) => {
      if (x.value < -REVEAL * 2.5 || e.velocityX < -1500) {
        x.value = withTiming(-600, { duration: 180 }, () => scheduleOnRN(onDelete));
      } else {
        x.value = withSpring(x.value < -REVEAL / 2 ? -REVEAL : 0, { velocity: e.velocityX, dampingRatio: 0.9 });
      }
    });
  const style = useAnimatedStyle(() => ({ transform: [{ translateX: x.value }] }));
  return (
    <Animated.View exiting={FadeOut.duration(150)} layout={LinearTransition.duration(200)}>
      <GestureDetector gesture={pan}>
        <Animated.View style={style}>{children}</Animated.View>
      </GestureDetector>
    </Animated.View>
  );
}
```

Check: scrolling vertically over the rows never opens one; the delete button is also reachable without the gesture (long-press menu or edit mode) and screen readers get an action (`accessibilityActions`).

## Collapsing header

The header keeps its height and moves up with `translateY`; only transform and opacity change, so scrolling stays smooth. The big title fades out first; the small one fades in after, with a gap so the two never overlap at half opacity. `Extrapolation.CLAMP` stops the header at its short state instead of sliding away.

```tsx
import { ReactNode } from 'react';
import Animated, { Extrapolation, interpolate, useAnimatedScrollHandler, useAnimatedStyle, useSharedValue } from 'react-native-reanimated';

const TALL = 140;
const SHORT = 56;

export function CollapsingScreen({ title, children }: { title: string; children: ReactNode }) {
  const offset = useSharedValue(0);
  const trackScroll = useAnimatedScrollHandler((e) => { offset.value = e.contentOffset.y; });
  const header = useAnimatedStyle(() => ({
    height: TALL, // fixed height; we move it, not resize it
    transform: [{ translateY: -interpolate(offset.value, [0, TALL - SHORT], [0, TALL - SHORT], Extrapolation.CLAMP) }],
  }));
  const bigTitle = useAnimatedStyle(() => ({
    opacity: interpolate(offset.value, [0, 40], [1, 0], Extrapolation.CLAMP),
  }));
  const smallTitle = useAnimatedStyle(() => ({
    opacity: interpolate(offset.value, [50, 80], [0, 1], Extrapolation.CLAMP),
  }));
  return (
    <>
      <Animated.ScrollView onScroll={trackScroll} scrollEventThrottle={16} contentContainerStyle={{ paddingTop: TALL }}>
        {children}
      </Animated.ScrollView>
      <Animated.View style={[{ position: 'absolute', top: 0, left: 0, right: 0 }, header]}>
        <Animated.Text accessibilityRole="header" style={[{ fontSize: 32, position: 'absolute', bottom: 12, left: 16 }, bigTitle]}>{title}</Animated.Text>
        <Animated.Text importantForAccessibility="no" style={[{ fontSize: 17, position: 'absolute', bottom: 16, alignSelf: 'center' }, smallTitle]}>{title}</Animated.Text>
      </Animated.View>
    </>
  );
}
```

On iOS with a native stack, try `headerLargeTitle: true` first; build this only when the design can't use it.

## List entrance

Rows rise 12 px and fade in. The delay caps at the sixth row, so a long list doesn't make the user wait for row forty. With Reduce Motion on, the row appears in place.

```tsx
import { Text } from 'react-native';
import Animated, { FadeInDown, ReduceMotion } from 'react-native-reanimated';

// Stagger only what fits the first screen; everything after arrives with no delay.
const entering = (index: number) =>
  FadeInDown.duration(260).delay(Math.min(index, 6) * 40).withInitialValues({ transform: [{ translateY: 12 }] })
    .reduceMotion(ReduceMotion.System);

export function Row({ index, label }: { index: number; label: string }) {
  return (
    <Animated.View entering={entering(index)}>
      <Text>{label}</Text>
    </Animated.View>
  );
}
```

Only animate entries on first load or when an item is added; skip it on scroll-back and on refresh of a list the user has already seen.

## Composer that rides the keyboard

The input bar moves with the keyboard frame by frame instead of jumping when it lands. Option A uses keyboard-controller (smoothest, handles interactive dismiss on iOS); option B uses Reanimated's own keyboard height when you'd rather not add a library.

```tsx
import { ReactNode } from 'react';
import { KeyboardStickyView } from 'react-native-keyboard-controller';
import Animated, { useAnimatedKeyboard, useAnimatedStyle } from 'react-native-reanimated';

// Option A: the composer rides the keyboard frame by frame (needs KeyboardProvider at the root).
export function Composer({ children }: { children: ReactNode }) {
  return <KeyboardStickyView offset={{ closed: 0, opened: 0 }}>{children}</KeyboardStickyView>;
}

// Option B: no extra library, Reanimated's own keyboard height.
export function ComposerB({ children }: { children: ReactNode }) {
  const kb = useAnimatedKeyboard();
  const style = useAnimatedStyle(() => ({ transform: [{ translateY: -kb.height.value }] }));
  return <Animated.View style={style}>{children}</Animated.View>;
}
```

Check: open and close the keyboard, drag it down on iOS, and rotate; the bar should never cover the field the user is typing in.

## Sliding tab indicator

Each tab reports where it is with `onLayout`; the pill springs to that spot and width. Measuring, not computing from the index, means tabs of different widths and translated labels still line up.

```tsx
import { useState } from 'react';
import { LayoutChangeEvent, Pressable, Text, View } from 'react-native';
import Animated, { useAnimatedStyle, useSharedValue, withSpring } from 'react-native-reanimated';

export function Segmented({ items, onChange }: { items: string[]; onChange: (i: number) => void }) {
  const [active, setActive] = useState(0);
  const pillX = useSharedValue(0);
  const pillW = useSharedValue(0);
  const boxes = useState<{ x: number; width: number }[]>([])[0];
  const go = (i: number) => {
    const b = boxes[i];
    if (!b) return;
    pillX.value = withSpring(b.x, { duration: 320, dampingRatio: 0.85 });
    pillW.value = withSpring(b.width, { duration: 320, dampingRatio: 0.85 });
    setActive(i);
    onChange(i);
  };
  const pill = useAnimatedStyle(() => ({ width: pillW.value, transform: [{ translateX: pillX.value }] }));
  return (
    <View accessibilityRole="tablist" style={{ flexDirection: 'row' }}>
      <Animated.View style={[{ position: 'absolute', top: 0, bottom: 0, borderRadius: 999 }, pill]} />
      {items.map((label, i) => (
        <Pressable
          key={label}
          accessibilityRole="tab"
          accessibilityState={{ selected: i === active }}
          onLayout={(e: LayoutChangeEvent) => {
            boxes[i] = e.nativeEvent.layout;
            if (i === active) { pillX.value = e.nativeEvent.layout.x; pillW.value = e.nativeEvent.layout.width; }
          }}
          onPress={() => go(i)}
          style={{ minHeight: 44, paddingHorizontal: 16, justifyContent: 'center' }}>
          <Text>{label}</Text>
        </Pressable>
      ))}
    </View>
  );
}
```

Check: long labels in another language and large text sizes; the pill should still fit its tab.

## Toast

Slides in from the top with a soft spring, fades out, and can be flicked up to dismiss. It announces itself to screen readers as a polite live region. The timing rules (how long it stays, one at a time, pausing while touched) are in `libraries-and-toasts.md`.

```tsx
import { Text } from 'react-native';
import { GestureDetector, Gesture } from 'react-native-gesture-handler';
import Animated, { FadeOut, SlideInUp, useAnimatedStyle, useSharedValue, withSpring } from 'react-native-reanimated';
import { scheduleOnRN } from 'react-native-worklets';

export function Toast({ message, onDismiss }: { message: string; onDismiss: () => void }) {
  const y = useSharedValue(0);
  const pan = Gesture.Pan()
    .onChange((e) => { y.value = Math.min(0, e.translationY); })
    .onEnd((e) => {
      if (y.value < -30 || e.velocityY < -500) scheduleOnRN(onDismiss);
      else y.value = withSpring(0);
    });
  const style = useAnimatedStyle(() => ({ transform: [{ translateY: y.value }] }));
  return (
    <GestureDetector gesture={pan}>
      <Animated.View
        accessibilityLiveRegion="polite"
        accessibilityRole="alert"
        entering={SlideInUp.springify().damping(18)}
        exiting={FadeOut.duration(150)}
        style={style}>
        <Text>{message}</Text>
      </Animated.View>
    </GestureDetector>
  );
}
```

## Fire once at a threshold

For pull to refresh, a sheet passing a snap point, or a slider crossing zero. The reaction watches a yes/no derived from the shared value and calls back only when that flips, so the haptic fires once per crossing instead of every frame.

```tsx
import * as Haptics from 'expo-haptics';
import { SharedValue, useAnimatedReaction } from 'react-native-reanimated';
import { scheduleOnRN } from 'react-native-worklets';

// Fires once each time the value crosses the line, in either direction; never every frame.
export function useThreshold(value: SharedValue<number>, line: number, onCross: (above: boolean) => void) {
  useAnimatedReaction(
    () => value.value > line,
    (above, was) => {
      if (was !== null && above !== was) scheduleOnRN(onCross, above);
    },
    [line],
  );
}

export const tick = () => Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
```

Use it as `useThreshold(y, 80, (above) => { if (above) tick(); })`.
