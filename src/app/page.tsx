// app/blog/[slug]/page.tsx
const Page = async ({ params }: { params: Promise<{ slug: string }> }) => {
  const { slug } = await params;

  return <html><body>
    <div>Post: {slug}</div>
  </body></html>;
};

export default Page;