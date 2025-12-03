'use client';

import { signIn } from 'next-auth/react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

interface SignInModalProps {
  onClose: () => void;
}

export default function SignInModal({ onClose }: SignInModalProps) {
  const showGoogleSignIn = process.env.NEXT_PUBLIC_GOOGLE_ENABLED !== 'false';
  const showEmailSignIn = process.env.NEXT_PUBLIC_EMAIL_ENABLED !== 'false';

  return (
    <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center">
      <Card className="p-8 max-w-md w-full text-center">
        <h3 className="card-title mb-4">Sign In to Continue</h3>
        <p className="helper-text mb-6">
          NexSupply is in early alpha. To protect our servers, anonymous users can only run 1 free analysis per day. Sign in to continue.
        </p>
        <div className="space-y-4">
          {showGoogleSignIn && (
            <Button onClick={() => signIn('google')} className="w-full" size="lg">
              Continue with Google
            </Button>
          )}
          {showEmailSignIn && (
            <Button onClick={() => signIn('email')} className="w-full" size="lg" variant={showGoogleSignIn ? "outline" : "primary"}>
              Continue with Email
            </Button>
          )}
          {!showGoogleSignIn && !showEmailSignIn && (
            <p className="text-sm text-muted-foreground">
              Authentication is not configured. Please contact support.
            </p>
          )}
        </div>
        <Button variant="ghost" onClick={onClose} className="mt-4">
          Maybe later
        </Button>
      </Card>
    </div>
  );
}