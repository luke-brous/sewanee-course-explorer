import { NextResponse } from 'next/server';
import prisma from '@/lib/prisma';

export async function GET() {
  try {
    // Fetch 10 courses to verify the data you uploaded via Python
    const courses = await prisma.course.findMany({
      take: 10,
      orderBy: {
        title: 'asc',
      },
    });

    return NextResponse.json(courses);
  } catch (error) {
    // Factor XI: Logs - Treat logs as event streams
    console.error('Database fetch error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch courses' },
      { status: 500 }
    );
  }
}