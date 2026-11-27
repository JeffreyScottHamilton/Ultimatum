'use client';
import { debounce } from 'lodash';
import { PrismaClient } from '@prisma/client';
import MonacoEditor from '@monaco-editor/react';
import { useEffect, useState } from 'react';

export default function Page({ id, first, last, items, ids }) {
  const [fullName, setFullName] = useState('');
  const [pos, setPos] = useState({ x: 0, y: 0 });
  useEffect(() => setFullName(`${first} ${last}`), [first, last]);

  function Row({ it }) {
    return <li>{it.name}</li>;
  }

  return (
    <Ctx.Provider value={{ items, add }}>
      <div onPointerMove={e => setPos({ x: e.clientX, y: e.clientY })}>
        <ul>{items.map((it, i) => <Row key={i} it={it} />)}</ul>
      </div>
    </Ctx.Provider>
  );
}
