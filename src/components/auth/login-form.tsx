
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginSchema, type LoginFormData, barcodeLoginSchema, type BarcodeLoginFormData } from "@/lib/schemas/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/hooks/use-auth";
import { Loader2, Camera, AlertTriangle } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import React, { useState, useEffect, useRef } from "react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { useToast } from "@/hooks/use-toast";

// Simple Google Icon SVG
const GoogleIcon = () => (
  <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" className="mr-2 h-5 w-5">
    <g><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"></path><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"></path><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"></path><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"></path><path fill="none" d="M0 0h48v48H0z"></path></g>
  </svg>
);


export function LoginForm() {
  const { signInWithEmail, signInWithBarcode, signInWithGoogle, loading: authLoading, error: authError, setError: setAuthError } = useAuth();
  const { toast } = useToast();

  const [hasCameraPermission, setHasCameraPermission] = useState<boolean | null>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const [activeTab, setActiveTab] = useState("email");


  const emailForm = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const barcodeForm = useForm<BarcodeLoginFormData>({
    resolver: zodResolver(barcodeLoginSchema),
    defaultValues: {
      barcodeValue: "",
    },
  });

  useEffect(() => {
    let activeStream: MediaStream | null = null;

    const startCamera = async () => {
      if (hasCameraPermission === false) { 
        return;
      }
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        activeStream = stream;
        setHasCameraPermission(true);
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (error) {
        console.error('Error accessing camera:', error);
        setHasCameraPermission(false);
        toast({
          variant: 'destructive',
          title: 'Camera Access Denied',
          description: 'Please enable camera permissions in your browser settings to use this feature.',
        });
      }
    };

    if (activeTab === 'barcode') {
      if (hasCameraPermission === null || hasCameraPermission === true) {
        startCamera();
      }
    }

    return () => { 
      if (activeStream) {
        activeStream.getTracks().forEach(track => track.stop());
      }
      if (videoRef.current) {
        if (videoRef.current.srcObject) {
            const currentStream = videoRef.current.srcObject as MediaStream;
            currentStream?.getTracks().forEach(track => track.stop());
            videoRef.current.srcObject = null;
        }
      }
    };
  }, [activeTab, toast, hasCameraPermission]); 


  const onEmailSubmit = async (data: LoginFormData) => {
    setAuthError(null);
    await signInWithEmail(data);
  };

  const onBarcodeSubmit = async (data: BarcodeLoginFormData) => {
    setAuthError(null);
    await signInWithBarcode(data.barcodeValue);
  };

  const handleGoogleSignIn = async () => {
    setAuthError(null);
    await signInWithGoogle();
  };
  
  useEffect(() => {
    if (authError) {
      // Check if the error is already displayed by a specific form. If not, or if it's a general error, show it.
      // This logic might need refinement based on how errors are set by signInWithGoogle if it doesn't use form.setError
      const emailFormError = emailForm.formState.errors.root?.message;
      const barcodeFormError = barcodeForm.formState.errors.root?.message;

      if (activeTab === "email" && !emailFormError) {
        emailForm.setError("root", { type: "manual", message: authError });
      } else if (activeTab === "barcode" && !barcodeFormError) {
        barcodeForm.setError("root", { type: "manual", message: authError });
      } else if (activeTab !== "email" && activeTab !== "barcode" && !emailFormError && !barcodeFormError) {
        // If Google sign-in fails, it won't set errors on email/barcode forms.
        // We can show a general toast or a dedicated error display area for Google sign-in if needed.
        // For now, the AuthProvider's toast will handle displaying the Google sign-in error.
        // If we want to show it in the form card, we might need a dedicated state here.
      }
    }
  }, [authError, activeTab, emailForm, barcodeForm]);


  return (
    <Card className="w-full max-w-md shadow-xl">
      <CardHeader>
        <CardTitle className="text-2xl">Login to Class Companion</CardTitle>
        <CardDescription>Access your timetable and study tools.</CardDescription>
      </CardHeader>
      <CardContent>
        <Button 
          variant="outline" 
          className="w-full mb-4" 
          onClick={handleGoogleSignIn}
          disabled={authLoading}
        >
          {authLoading ? (
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          ) : (
            <GoogleIcon />
          )}
          Sign in with Google
        </Button>

        <div className="my-4 flex items-center">
          <div className="flex-grow border-t border-muted"></div>
          <span className="mx-4 text-xs uppercase text-muted-foreground">Or</span>
          <div className="flex-grow border-t border-muted"></div>
        </div>

        <Tabs defaultValue="email" className="w-full" onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="email">Email & Password</TabsTrigger>
            <TabsTrigger value="barcode">Scan Barcode</TabsTrigger>
          </TabsList>
          
          <TabsContent value="email">
            <Form {...emailForm}>
              <form onSubmit={emailForm.handleSubmit(onEmailSubmit)} className="space-y-6 pt-6">
                <FormField
                  control={emailForm.control}
                  name="email"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Email</FormLabel>
                      <FormControl>
                        <Input type="email" placeholder="you@example.com" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={emailForm.control}
                  name="password"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Password</FormLabel>
                      <FormControl>
                        <Input type="password" placeholder="••••••••" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                {emailForm.formState.errors.root && (
                     <FormMessage className="text-destructive text-sm pt-0">
                        {emailForm.formState.errors.root.message}
                     </FormMessage>
                )}
                <Button type="submit" className="w-full" disabled={authLoading || emailForm.formState.isSubmitting}>
                  {authLoading || emailForm.formState.isSubmitting ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Signing In...
                    </>
                  ) : (
                    "Login with Email"
                  )}
                </Button>
              </form>
            </Form>
          </TabsContent>

          <TabsContent value="barcode">
            <div className="space-y-6 pt-6">
              <div className="flex flex-col items-center space-y-4">
                 <p className="text-sm text-muted-foreground text-center">
                    Position your barcode in front of the camera, or enter the value manually below.
                  </p>
                <div className="w-full max-w-xs aspect-video bg-muted rounded-md overflow-hidden flex items-center justify-center">
                  <video ref={videoRef} className="w-full h-full object-cover" autoPlay muted playsInline />
                   {hasCameraPermission === false && (
                     <div className="absolute p-4 text-center text-destructive-foreground bg-destructive/80 rounded-md">
                        <Camera className="h-8 w-8 mx-auto mb-2"/>
                        Camera access denied.
                     </div>
                   )}
                   {hasCameraPermission === null && videoRef.current && !videoRef.current.srcObject && ( 
                     <div className="absolute p-4 text-center text-muted-foreground">
                        <Loader2 className="h-8 w-8 mx-auto mb-2 animate-spin"/>
                        Requesting camera...
                     </div>
                   )}
                </div>
                {hasCameraPermission === false && (
                    <Alert variant="destructive" className="w-full max-w-xs">
                      <AlertTriangle className="h-4 w-4" />
                      <AlertTitle>Camera Access Required</AlertTitle>
                      <AlertDescription>
                        Please allow camera access in your browser settings to use barcode scanning. You can still enter the barcode value manually.
                      </AlertDescription>
                    </Alert>
                )}
                 <p className="text-xs text-muted-foreground p-2 bg-primary/10 rounded-md border border-primary/50">
                    <b>Demo Note:</b> For this prototype, manually enter <b><code>8918</code></b> or <b><code>8946</code></b> in the field below.
                    Ensure the demo user (email: <code>barcodeuser@example.com</code>, password: <code>password123</code>) exists in your Firebase project.
                  </p>
              </div>

              <Form {...barcodeForm}>
                <form onSubmit={barcodeForm.handleSubmit(onBarcodeSubmit)} className="space-y-4">
                  <FormField
                    control={barcodeForm.control}
                    name="barcodeValue"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Barcode Value</FormLabel>
                        <FormControl>
                          <Input placeholder="Manually enter barcode value" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  {barcodeForm.formState.errors.root && (
                     <FormMessage className="text-destructive text-sm pt-0">
                        {barcodeForm.formState.errors.root.message}
                     </FormMessage>
                  )}
                  <Button type="submit" className="w-full" disabled={authLoading || barcodeForm.formState.isSubmitting}>
                    {authLoading || barcodeForm.formState.isSubmitting ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Verifying Barcode...
                      </>
                    ) : (
                      "Login with Barcode"
                    )}
                  </Button>
                </form>
              </Form>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}
