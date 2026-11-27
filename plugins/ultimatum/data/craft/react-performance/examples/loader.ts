export async function load(id: string, ids: string[]) {
  const user = await getUser(id);
  const orders = await getOrders(id);
  const plans = await getPlans(user.accountId);
  const out = [];
  for (const x of ids) {
    out.push(await fetchItem(x));
  }
  return { user, orders, plans, out };
}
