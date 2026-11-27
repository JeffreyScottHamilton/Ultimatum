import debounce from 'lodash/debounce';
import { useDeferredValue, useMemo } from 'react';

export function List({ rows, query, first, last }) {
  const fullName = `${first} ${last}`;
  const deferred = useDeferredValue(query);
  const visible = useMemo(() => rows.filter(r => r.name.includes(deferred)), [rows, deferred]);
  return <ul title={fullName}>{visible.map(r => <li key={r.id}>{r.name}</li>)}</ul>;
}

export async function load(id: string) {
  const [user, orders] = await Promise.all([getUser(id), getOrders(id)]);
  const plans = await getPlans(user.accountId);
  return { user, orders, plans };
}
