
import * as z from "zod";

export const loginSchema = z.object({
  email: z.string().email({ message: "Invalid email address." }),
  password: z.string().min(6, { message: "Password must be at least 6 characters." }),
});
export type LoginFormData = z.infer<typeof loginSchema>;


export const barcodeLoginSchema = z.object({
  barcodeValue: z.string().min(1, { message: "Barcode value cannot be empty." }),
});
export type BarcodeLoginFormData = z.infer<typeof barcodeLoginSchema>;


// Optional: Registration schema if you add registration later
export const registrationSchema = z.object({
  email: z.string().email({ message: "Invalid email address." }),
  password: z.string().min(6, { message: "Password must be at least 6 characters." }),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords do not match.",
  path: ["confirmPassword"],
});

export type RegistrationFormData = z.infer<typeof registrationSchema>;
